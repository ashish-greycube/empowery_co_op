from __future__ import unicode_literals
import frappe
from frappe.sessions import Session
from frappe.utils import flt, has_common

@frappe.whitelist()
def set_portal_homepage(login_manager):
	logged_in_user_roles=frappe.get_roles(frappe.local.session_obj.user)
	co_op_supplier_roles=["Coop-Supplier", "Supplier", "All", "Guest"]
	co_op_customer_roles=["Coop-Customer", "Customer", "All", "Guest"]
	if (len(logged_in_user_roles)==len(set(logged_in_user_roles).intersection(set(co_op_supplier_roles)))  or len(logged_in_user_roles)==len(set(logged_in_user_roles).intersection(set(co_op_customer_roles)))):
		frappe.local.response["home_page"] = "/me"

@frappe.whitelist()
def get_linked_supplier(custname):
 	return frappe.db.sql("""select parenttype,parent,DATE_FORMAT(creation,'%%M-%%d-%%Y') as join_date from `tabDynamic Link` where parenttype='Supplier' and docstatus=0 and parentfield='links' and link_doctype='Customer' and link_name = %s order by join_date desc""" ,custname, as_dict=1) or 0

@frappe.whitelist()
def get_linked_customer(suppname):
 	return frappe.db.sql("""select link_doctype,link_name,DATE_FORMAT(creation,'%%M-%%d-%%Y') as join_date from `tabDynamic Link` where link_doctype='Customer' and parenttype='Supplier'and docstatus = 0 and parent=%s order by join_date desc """ ,suppname, as_dict=1) or 0