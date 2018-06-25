# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def execute(useremail):
	columns, data = [], []
	
	suppname=get_session_supplier(useremail)
	if suppname==[]:
		return  data
	suppname= suppname[0]['supplier']
	columns = get_columns()


	

	linked_list = get_linked(suppname)
	nonlinked_list = get_nonlinked(suppname)

	for customer in linked_list:
		row = []
		row = [customer.customer_name,customer.customer_primary_contact,customer.mobile_no,customer.email_id,customer.linked]
		data.append(row)

	for customer in nonlinked_list:
		row = []
		row = [customer.customer_name,customer.customer_primary_contact,customer.mobile_no,customer.email_id,customer.linked]
		data.append(row)
	print data
	return data


def get_columns():
	columns = [
		("Customer") + ":Data:270",
		("Primary Contact") + ":Data:220",		
		("Mobile No") + ":Data:130",
		("Email ID") + ":Data:230",	
		("Linked") + ":Check:50"
	]
	return columns

def get_linked(suppname):
	return frappe.db.sql("""select * from 
(
select a.customer_name, concat(IFNULL(d.first_name,''),' ',IFNULL(d.last_name,'')) as customer_primary_contact, d.email_id, d.mobile_no, 1 as linked, 
ROW_NUMBER() over (PARTITION by a.customer_name ORDER by c.creation) as rn
from `tabCustomer` a 
inner join `tabDynamic Link` b on b.link_doctype='Customer' and b.parenttype='Supplier' and b.docstatus = 0 and b.parent=
 %s and b.link_name=a.customer_name
left outer join `tabDynamic Link` c on c.link_doctype='Customer' and c.parenttype='Contact' and c.link_name=a.customer_name
left outer join tabContact d on d.name = c.parent and d.is_primary_contact =1
where a.customer_group !='Supplier'
) t where t.rn=1""", suppname, as_dict=1)
	
def get_nonlinked(suppname):
	return frappe.db.sql("""select * from 
(select a.customer_name, 0 as linked, concat(IFNULL(d.first_name,''),' ',IFNULL(d.last_name,'')) customer_primary_contact, d.email_id, d.mobile_no,
ROW_NUMBER() over (PARTITION by a.customer_name ORDER by c.creation) as rn
from `tabCustomer` a 
left outer join `tabDynamic Link` c on c.link_doctype='Customer' and c.parenttype='Contact' and c.link_name=a.customer_name
left outer join tabContact d on d.name = c.parent and d.is_primary_contact =1
where a.customer_group !='Supplier' 
and not exists 
(select 1 from `tabDynamic Link` b 
where b.parent=%s and b.link_doctype='Customer' and b.parenttype='Supplier' and b.docstatus = 0 and b.link_name=a.customer_name)
) t where t.rn=1""", suppname, as_dict=1)

@frappe.whitelist()
def get_session_supplier(useremail):
 	return frappe.db.sql("""select link_name as supplier from `tabDynamic Link` where link_doctype="Supplier" and parenttype="Contact" and parent in(
 select name from `tabContact` where user = %s)""" ,useremail, as_dict=1)