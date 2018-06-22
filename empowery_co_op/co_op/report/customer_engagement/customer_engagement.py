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
		conditions += "and parent= %(supplier)s"

	return frappe.db.sql("""select customer_name,customer_primary_contact,mobile_no,email_id, 1 as linked from `tabCustomer`
where customer_group !='Supplier' and name in (select link_name from `tabDynamic Link` where link_doctype='Customer' and parenttype='Supplier' and  docstatus = 0 %s ) order by linked,customer_name,customer_primary_contact""" % conditions, filters, as_dict=1)
	
def get_nonlinked(filters):
	conditions = ""

	if filters.get("supplier"):
		conditions += "and parent= %(supplier)s"

	return frappe.db.sql("""select customer_name,customer_primary_contact,mobile_no,email_id, 0 as linked from `tabCustomer`
where customer_group !='Supplier' and name not in (select link_name from `tabDynamic Link` where link_doctype='Customer' and parenttype='Supplier' and  docstatus = 0 %s ) order by linked,customer_name,customer_primary_contact""" % conditions, filters, as_dict=1)

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
