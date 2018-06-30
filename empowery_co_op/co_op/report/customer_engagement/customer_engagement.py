# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data =  get_columns(), []
	if filters != {}:
		suppname=filters.get("supplier")
		linked_list = get_linked(filters)
		nonlinked_list = get_nonlinked(filters)
		for customer in linked_list:
			row = []
			row = [customer.customer_name,customer.customer_primary_contact,customer.mobile_no,customer.email_id,customer.linked,"""
      <input type="button"  class="btn btn-primary  btn-xs" value="Remove" onclick="frappe.remove_party_link('%s', '%s')">"""% (customer.customer_name,suppname)]
			data.append(row)

		for customer in nonlinked_list:
			row = []
			row = [customer.customer_name,customer.customer_primary_contact,customer.mobile_no,customer.email_id,customer.linked,"""
    <input type="button"  class="btn btn-primary  btn-xs" value="Add" onclick="frappe.add_party_link('%s', '%s', '%s')">"""% (customer.customer_name,suppname,customer.linked)]
			data.append(row)
	return columns, data

def get_columns():
	columns = [
		("Customer") + ":Data:270",
		("Primary Contact") + ":Data:220",		
		("Mobile No") + ":Data:130",
		("Email ID") + ":Data:230",	
		("Linked") + ":Check:50",
		("Action") + ":HTML:70"
		
	]
	return columns

def get_linked(filters):
	conditions = ""

	if filters.get("supplier"):
		conditions += " and b.parent= %(supplier)s"

	return frappe.db.sql("""select a.customer_name, concat(IFNULL(d.first_name,''),' ',IFNULL(d.last_name,'')) as customer_primary_contact, d.email_id, d.mobile_no, 1 as linked
from `tabCustomer` a 
inner join `tabDynamic Link` b on b.link_doctype='Customer' and b.parenttype='Supplier' and b.docstatus = 0 
and b.link_name=a.customer_name %s
left outer join `tabDynamic Link` l on l.link_doctype='Customer' and l.parenttype='Contact'
left outer join 
(
	select a.customer_name, max(l.name) link
	from `tabCustomer` a
	inner join `tabDynamic Link` l on l.link_doctype='Customer' 
	and l.parenttype='Contact' and l.link_name = a.customer_name
	group by a.customer_name
) c on c.link = l.name and a.customer_name=c.customer_name
left outer join tabContact d on d.name = l.parent and d.is_primary_contact =1
where a.customer_group !='Supplier' and c.link is not null""" % conditions, filters, as_dict=1)
	
def get_nonlinked(filters):
	conditions = ""

	if filters.get("supplier"):
		conditions += " and b.parent= %(supplier)s"

	return frappe.db.sql("""select a.customer_name, 0 as linked, concat_ws(' ',c.first_name,c.last_name) customer_primary_contact, c.email_id, c.mobile_no
from
(
	select a.customer_name
	from `tabCustomer` a
	where  a.customer_group !='Supplier' and not exists (select 1 from `tabDynamic Link` b where b.link_doctype='Customer' and b.parenttype='Supplier' 
	and b.docstatus = 0 and b.link_name=a.customer_name %s)
) a
left outer join 
(	select a.customer_name, max(d.name) contact
	from `tabCustomer` a
	inner join `tabDynamic Link` l on l.link_doctype='Customer' 
	and l.parenttype='Contact' and l.link_name = a.customer_name
	left outer join tabContact d on d.name = l.parent and d.is_primary_contact =1
	group by a.customer_name
) b on a.customer_name = b.customer_name
left outer join tabContact c on c.name = b.contact""" % conditions, filters, as_dict=1)

@frappe.whitelist()
def add_party_link(custname, suppname,isLinked):
	if ((custname !=None) and (suppname !=None) and (isLinked == '0')):	
		supplier=frappe.get_doc('Supplier', suppname)
		supplier.append('links', dict(link_doctype='Customer', link_name=custname))
		supplier.save(ignore_permissions=True)	

@frappe.whitelist()
def remove_party_link(custname, suppname):
	if custname !=None and suppname !=None :		
		parenttype='Supplier'
		name = frappe.db.sql_list("""delete from `tabDynamic Link`  where  parenttype=%s and link_doctype='Customer' and link_name=%s and parent=%s""",
			(parenttype, custname, suppname))
