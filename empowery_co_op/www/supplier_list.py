from __future__ import unicode_literals
import frappe, json
from frappe.utils import split_emails
from frappe import _
import email

def get_context(context):
    context.no_cache = 1
    # setup vendor slideshow
    vendor_slideshow_doc = frappe.get_single('Vendor Offer')
    if vendor_slideshow_doc.slideshow:
        slideshow = frappe.get_doc("Website Slideshow", vendor_slideshow_doc.slideshow)
        context.slideshow=vendor_slideshow_doc.slideshow
        context.update({
            "slides": slideshow.get({"doctype":"Website Slideshow Item"}),
            "slideshow_header": slideshow.header or ""
        })

    # setup vendor category list and disclaimer page
    context.vendor_category_list=frappe.db.sql("""select distinct(category.service_category) as service_category from `tabService Category Detail` category
            inner join `tabSupplier` supplier on category.parent=supplier.name
            where category.parentfield='service_category' and supplier.display_on_partner_listing_page=1
            order by category.service_category""",as_dict=1)
    context.disclaimer_web_page = 'vendor_disclaimer.html'

# setup vendor category list
    vendor_categories=frappe.db.sql("""select supplier.name,category.service_category as service_category from `tabService Category Detail` category
inner join `tabSupplier` supplier on category.parent=supplier.name
where category.parentfield='service_category' and supplier.display_on_partner_listing_page=1
order by supplier.name,category.service_category""",as_dict=1)
   
    suppliers = {}
    for d in vendor_categories:
        if not suppliers.get(d['name'],None):
            suppliers[d['name']] = []
        suppliers[d['name']].append(d['service_category'])
    for key in suppliers:
        suppliers[key] = "|".join(set(suppliers[key]))

    context.supplier_category=suppliers

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
    vendor_offer_doc = frappe.get_single('Vendor Offer')
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