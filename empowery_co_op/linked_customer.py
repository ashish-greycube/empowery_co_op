# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def execute(useremail):
	
	suppname=get_session_supplier(useremail)
	print("-------------------------------------")
	suppname= suppname[0]['supplier']
	columns, data = [], []
	columns = get_columns()
	if suppname=={}:
		print data
		return  data

	

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
	return frappe.db.sql("""select customer_name,customer_primary_contact,mobile_no,email_id, 1 as linked from `tabCustomer`
where customer_group !='Supplier' and name in (select link_name from `tabDynamic Link` where link_doctype='Customer' and parenttype='Supplier' and  docstatus = 0 and parent= %s )""", suppname, as_dict=1)
	
def get_nonlinked(suppname):
	return frappe.db.sql("""select customer_name,customer_primary_contact,mobile_no,email_id, 0 as linked from `tabCustomer`
where customer_group !='Supplier' and name not in (select link_name from `tabDynamic Link` where link_doctype='Customer' and parenttype='Supplier' and  docstatus = 0 and parent=%s )""",suppname, as_dict=1)

@frappe.whitelist()
def get_session_supplier(useremail):
 	return frappe.db.sql("""select link_name as supplier from `tabDynamic Link` where link_doctype="Supplier" and parenttype="Contact" and parent in(
 select name from `tabContact` where user = %s)""" ,useremail, as_dict=1)