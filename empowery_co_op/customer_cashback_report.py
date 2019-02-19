# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr

@frappe.whitelist()
def execute(useremail,customer_company):
	columns, data = [], []

	useremail=get_session_customer(useremail)
	if useremail == []:
		return  data
	if customer_company==None or customer_company=='':
		customer_company=useremail[0]["customer"]
	
	columns = get_columns()



	linked_list = get_linked(customer_company)
	print '--------------------------------------------------'
	print linked_list
	# nonlinked_list = get_nonlinked(customer_company)
	customer=useremail[0]["customer"]
	
	for d in linked_list:
		row = []
		row = [d.Customer,d.Grand_Total_Cashback,d.Month_Year]
		data.append(row)


	return  data

def get_columns():
	columns = [
		("Customer") + ":Data:150",
		("Grand Total Cashback") + ":Data:120",
		("Month-Year") + ":Data:100"
	]
	return columns

def get_linked(customer_company):
	return frappe.db.sql("""SELECT SI.customer_name as Customer,  sum(SIT.base_net_amount) as Grand_Total_Cashback, 
CONCAT( MONTHNAME(SI.posting_date),"-",YEAR(SI.posting_date) ) AS Month_Year 
from `tabSales Invoice` as SI inner join `tabSales Invoice Item` as SIT ON SIT.parent = SI.name where SIT.item_name IN 
( SELECT parent from `tabItem Customer Detail` where customer_name = %s) group by SI.customer_name,SIT.base_net_amount, SIT.item_name, CONCAT( MONTHNAME(SI.posting_date),"-",YEAR(SI.posting_date) ) 
ORDER BY CONCAT( MONTHNAME(SI.posting_date),"-",YEAR(SI.posting_date) ) and SI.docstatus = 1
	""",customer_company, as_dict=1)

@frappe.whitelist()
def get_session_customer(useremail):
 	return frappe.db.sql("""select link_name as customer from `tabDynamic Link` where link_doctype="Customer" and parenttype="Contact" and parent in(
 select name from `tabContact` where user = %s)""" ,useremail, as_dict=1)
