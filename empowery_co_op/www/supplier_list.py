from __future__ import unicode_literals
import frappe, json
from frappe.utils import split_emails
from frappe import _
import email
from frappe.modules import get_module_path, scrub

def get_context(context):
    context.no_cache = 1
    print 
    print frappe.form_dict
    # setup vendor slideshow
    vendor_slideshow_doc = frappe.get_single('Vendor Carousel and Email template')
    if vendor_slideshow_doc.slideshow:
        slideshow = frappe.get_doc("Website Slideshow", vendor_slideshow_doc.slideshow)
        context.slideshow=vendor_slideshow_doc.slideshow
        context.update({
            "slides": slideshow.get({"doctype":"Website Slideshow Item"}),
            "slideshow_header": slideshow.header or ""
        })

# setup selection dropdown vendor category list
    vendor_categories=frappe.db.sql("""select distinct(service_category) from `tabSupplier` where service_category is not null""",as_dict=1)
    context.vendor_category_list=vendor_categories

# setup selection dropdown vendor location list
    vendor_locations=frappe.db.sql("""select distinct(location.geo_location) as location_category from `tabSupplier Geo Location Detail` location
inner join `tabSupplier` supplier on location.parent=supplier.name
where location.parentfield='geo_location' and supplier.display_on_partner_listing_page=1
order by supplier.name,location.geo_location""",as_dict=1)
    context.vendor_location_list=vendor_locations

# setup vendor geo location list
    vendor_location=frappe.db.sql("""select supplier.name,supplier.service_category,location.geo_location as location_category from `tabSupplier Geo Location Detail` location
inner join `tabSupplier` supplier on location.parent=supplier.name
where location.parentfield='geo_location' and supplier.display_on_partner_listing_page=1
order by supplier.name,location.geo_location""",as_dict=1)
   
    vendor_without_location=frappe.db.sql("""select supplier.name,supplier.service_category from `tabSupplier` supplier 
    where supplier.name not in( select distinct(parent) from `tabSupplier Geo Location Detail`) and supplier.service_category is not null""",as_dict=1)

    suppliers = {}
    for d in vendor_location:
        if not suppliers.get(d['name'],None):
            suppliers[d['name']] = []
            suppliers[d['name']].append('all_category_all_location')
            suppliers[d['name']].append(scrub(d['service_category']).replace('/','sub').replace('&','and')+'_'+'all_location')
        suppliers[d['name']].append(scrub(d['service_category']).replace('/','sub').replace('&','and')+'_'+scrub(d['location_category']).replace('/','sub').replace('&','and'))
        suppliers[d['name']].append('all_category'+'_'+scrub(d['location_category']).replace('/','sub').replace('&','and'))

    for d in vendor_without_location:
        if not suppliers.get(d['name'],None):
            suppliers[d['name']] = []
            suppliers[d['name']].append('all_category_all_location')
            suppliers[d['name']].append(scrub(d['service_category']).replace('/','sub').replace('&','and')+'_'+'all_location')  

    for key in suppliers:
        suppliers[key] = "|".join(set(suppliers[key]))

    print suppliers
    context.location_category=suppliers

    #setup form fill up data
    if frappe.session.user!='Guest':
        context.form_data=frappe.db.sql("""select customer.link_name as company,IF(contact.phone IS NULL or contact.phone = '', contact.mobile_no, contact.phone) as phone
            from `tabContact` contact
            inner join `tabDynamic Link` customer on
            customer.parent=contact.name
            where customer.link_doctype='Customer' and customer.parenttype='Contact'
            and contact.user=%s""",frappe.session.user,as_dict=1)
        if len(context.form_data)!=0:
            context.form_data=context.form_data[0]
        else:
            context.form_data=0

    # setup vedor data
    if frappe.session.user=='Guest':
        context.vendor_supplier = frappe.db.sql("""select name,supplier_type,image,service_category,offer_headline,offer_expiration_date,offer_summary,'guest' as more_details,geo_eligibility
        from `tabSupplier`
        where display_on_partner_listing_page=1 and
        supplier_type ='Supplier Partner' order by name""",as_dict=1)

        context.vendor_affiliate = frappe.db.sql("""select name,supplier_type,image,service_category,offer_headline,offer_expiration_date,offer_summary,'guest' as more_details,geo_eligibility
        from `tabSupplier`
        where display_on_partner_listing_page=1 and
        supplier_type ='Affiliate Partner' order by name""",as_dict=1)

    else:
        context.vendor_supplier = frappe.db.sql("""select name,supplier_type,image,service_category,offer_headline,offer_expiration_date,offer_summary,more_details as more_details ,geo_eligibility,disclaimer_details,contact_email_for_offers
        from `tabSupplier`
        where display_on_partner_listing_page=1 and
        supplier_type ='Supplier Partner' order by name""",as_dict=1)

        context.vendor_affiliate = frappe.db.sql("""select name,supplier_type,image,service_category,offer_headline,offer_expiration_date,offer_summary,more_details as more_details,geo_eligibility,disclaimer_details,contact_email_for_offers
        from `tabSupplier`
        where display_on_partner_listing_page=1 and
        supplier_type ='Affiliate Partner' order by name""",as_dict=1)

@frappe.whitelist(allow_guest=True)
def send_email(name,company,email,phone,is_guest,vendor_list):
    vendor_offer_doc = frappe.get_single('Vendor Carousel and Email template')
    raw_subject=vendor_offer_doc.subject
    raw_email=vendor_offer_doc.email

    raw_vendor_list=json.loads(vendor_list)
    
    for vendor in raw_vendor_list:
        subject=raw_subject.replace('{sender_name}', name).replace('{sender_company}',company).replace('{sender_email}',email).replace('{sender_phone}',phone).replace('{sender_is_guest}',is_guest).replace('{vendor_name}',vendor)
        email=raw_email.replace('{sender_name}', name).replace('{sender_company}',company).replace('{sender_email}',email).replace('{sender_phone}',phone).replace('{sender_is_guest}',is_guest).replace('{vendor_name}',vendor)
        vendor_email= frappe.db.sql("""select contact_email_for_offers from  `tabSupplier` where name=%s""",vendor,as_dict=1)
        # outgoing_email_id = frappe.get_doc("Email Account", {"default_outgoing": "1"})
        # if outgoing_email_id:
        recipients = split_emails(frappe.db.get_value("Supplier", filters={"name": vendor}, fieldname="contact_email_for_offers"))
        
        frappe.sendmail(recipients=recipients, message=email, subject=subject, now=True)
        recipients=None
        email=None
        subject=None
    return

