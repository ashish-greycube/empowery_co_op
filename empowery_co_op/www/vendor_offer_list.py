from __future__ import unicode_literals
import frappe, json
from frappe.utils import split_emails
from frappe import _
import email
from frappe.modules import get_module_path, scrub

def get_context(context):
    context.no_cache = 1
    # setup vendor slideshow
    vendor_slideshow_doc = frappe.get_single('Vendor Carousel and Email template')
    if vendor_slideshow_doc.slideshow:
        slideshow = frappe.get_doc("Website Slideshow", vendor_slideshow_doc.slideshow)
        context.slideshow=vendor_slideshow_doc.slideshow
        context.update({
            "slides": slideshow.get({"doctype":"Website Slideshow Item"}),
            "slideshow_header": slideshow.header or ""
        })

# setup selection dropdown for vendor category
    vendor_categories=frappe.db.sql("""select distinct(service_category) from `tabSupplier`
     where service_category is not null and supplier_type in ('Affiliate Partner','Supplier Partner')""",as_dict=1)
    context.vendor_category_dropdown=vendor_categories

# setup selection dropdown for vendor location
    vendor_locations=frappe.db.sql("""select distinct(location.geo_location) as location_category from `tabSupplier Geo Location Detail` location
inner join `tabSupplier` supplier on location.parent=supplier.name
where location.parentfield='geo_location' and supplier.display_on_partner_listing_page=1
and supplier_type in ('Affiliate Partner','Supplier Partner')
order by supplier.name,location.geo_location""",as_dict=1)
    context.vendor_location_dropdown=vendor_locations

# setup vendor geo location list
    vendor_location=frappe.db.sql("""select supplier.name,supplier.service_category,location.geo_location as location_category 
from `tabSupplier` supplier 
INNER JOIN `tabSupplier Geo Location Detail` location
on location.parent=supplier.name
where supplier.display_on_partner_listing_page=1
and supplier_type in ('Affiliate Partner','Supplier Partner')
order by supplier.name,location.geo_location""",as_dict=1)
   
 
    suppliers = {}
    for d in vendor_location:
        if not suppliers.get(d['name'],None):
            suppliers[d['name']] = []
            suppliers[d['name']].append('[all_location]')
        if d['location_category']:
            suppliers[d['name']].append("["+d['location_category']+"]")
  
    for key in suppliers:
        suppliers[key] = " ".join(set(suppliers[key]))

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
        context.vendor_supplier = frappe.db.sql("""select name,supplier_type,image,service_category,offer_headline,offer_expiration_date,offer_summary,'guest' as more_details
        from `tabSupplier`
        where display_on_partner_listing_page=1 and
        supplier_type ='Supplier Partner' order by name""",as_dict=1)

        context.vendor_affiliate = frappe.db.sql("""select name,supplier_type,image,service_category,offer_headline,offer_expiration_date,offer_summary,'guest' as more_details
        from `tabSupplier`
        where display_on_partner_listing_page=1 and
        supplier_type ='Affiliate Partner' order by name""",as_dict=1)

    else:
        context.vendor_supplier = frappe.db.sql("""select name,supplier_type,image,service_category,offer_headline,offer_expiration_date,offer_summary,more_details as more_details,disclaimer_details,contact_email_for_offers
        from `tabSupplier`
        where display_on_partner_listing_page=1 and
        supplier_type ='Supplier Partner' order by name""",as_dict=1)

        context.vendor_affiliate = frappe.db.sql("""select name,supplier_type,image,service_category,offer_headline,offer_expiration_date,offer_summary,more_details as more_details,disclaimer_details,contact_email_for_offers
        from `tabSupplier`
        where display_on_partner_listing_page=1 and
        supplier_type ='Affiliate Partner' order by name""",as_dict=1)

@frappe.whitelist(allow_guest=True)
def send_email(name,email,phone,is_guest,vendor_list):
    vendor_offer_doc = frappe.get_single('Vendor Carousel and Email template')
    raw_subject=vendor_offer_doc.subject or ''
    raw_email=vendor_offer_doc.email or ''
    if is_guest==True:
        is_guest='No, user is a guest'
    else:
        is_guest='Yes, user is an existing member'
    raw_vendor_list=json.loads(vendor_list)
    count=0
    for vendor in raw_vendor_list:

        subject=raw_subject.replace('{sender_name}', name or "").replace('{sender_email}',email or "").replace('{sender_phone}',phone or "").replace('{sender_is_guest}',is_guest or "").replace('{vendor_name}',vendor or "")
        email=raw_email.replace('{sender_name}', name or "").replace('{sender_email}',email or "").replace('{sender_phone}',phone or "").replace('{sender_is_guest}',is_guest or "").replace('{vendor_name}',vendor or "")
        vendor_email= frappe.db.sql("""select contact_email_for_offers from  `tabSupplier` where name=%s""",vendor,as_dict=1)
        outgoing_email_id = frappe.get_doc("Email Account", {"default_outgoing": "1"})
        if outgoing_email_id:
            recipients = split_emails(frappe.db.get_value("Supplier", filters={"name": vendor}, fieldname="contact_email_for_offers"))
            frappe.sendmail(recipients=recipients, message=email, subject=subject)
            recipients=None
            subject=None
            email=None
            count=count+1
    return count

