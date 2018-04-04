# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()

	linked_list = get_linked(filters)
	nonlinked_list = get_nonlinked(filters)
	customer=filters.get("customer")
	
	for d in linked_list:
		row = []
		linked=1
		row = [d.parent,linked,"""
      <input type="button"  class="btn btn-primary  btn-xs" value="Remove" onclick="frappe.remove_party_link('%s', '%s')">"""% (customer,d.parent)]
		data.append(row)

	for d in nonlinked_list:
		row = []
		linked=0
		row = [d.name,linked,"""
    <input type="button"  class="btn btn-primary  btn-xs" value="Add" onclick="frappe.add_party_link('%s', '%s', '%s')">"""% (customer,d.name,linked)]
		data.append(row)

	return columns, data

def get_columns():
	columns = [
		("Supplier") + ":Data:120",
		("Linked") + ":Check:120",
		("Action") + ":HTML:120"
	]
	return columns

def get_linked(filters):
	conditions = ""

	if filters.get("customer"):
		conditions += "and link_name = %(customer)s"

	return frappe.db.sql("""select parent from `tabDynamic Link` where link_doctype='Customer' and parenttype='Supplier'and docstatus = 0 %s
	""" % conditions, filters, as_dict=1)

def get_nonlinked(filters):
	conditions = ""

	if filters.get("customer"):
		conditions += "and link_name = %(customer)s"

	return frappe.db.sql("""select `tabSupplier`.name AS name from `tabSupplier` where name not in (
select parent from `tabDynamic Link` where link_doctype='Customer' and docstatus = 0 %s
	)""" % conditions, filters, as_dict=1)

@frappe.whitelist()
def add_party_link(custname, suppname,isLinked):
	if custname !=None and suppname !=None and isLinked ==0:		
		supplier=frappe.get_doc('Supplier', suppname)
		supplier.append('links', dict(link_doctype='Customer', link_name=custname))
		supplier.save(ignore_permissions=True)	

@frappe.whitelist()
def remove_party_link(custname, suppname):
	if custname !=None and suppname !=None :		
		parenttype='Supplier'
		name = frappe.db.sql_list("""delete from `tabDynamic Link`  where  parenttype=%s and link_doctype='Customer' and link_name=%s and parent=%s""",
			(parenttype, custname, suppname))

@frappe.whitelist()
def get_session_customer(useremail):
 	return frappe.db.sql("""select link_name from `tabDynamic Link` where link_doctype="Customer" and parenttype="Contact" and parent in(
 select name from `tabContact` where user = %s)""" ,useremail, as_dict=1)
