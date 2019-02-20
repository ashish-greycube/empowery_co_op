# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr

@frappe.whitelist()
def execute(useremail,customer_company,filter_year):
	columns, data = [], []

	useremail=get_session_customer(useremail)
	if useremail == []:
		return  data
	if customer_company==None or customer_company=='':
		customer_company=useremail[0]["customer"]
	if filter_year==None or filter_year=='':
		filter_year=get_filter_year()[0]["year"]
	
	columns = get_columns()



	linked_list = get_linked(customer_company,filter_year)
	customer=useremail[0]["customer"]

	total_row =0.0
	
	for d in linked_list:
		row = []
		row = [d.Customer,d.Grand_Total_Cashback,d.Month_Year]
		total_row += d.Grand_Total_Cashback 
		data.append(row)
	data.append([])
	data.append(["Cashback Grand Total",total_row,""])
	return  data

def get_columns():
	columns = [
		("Customer") + ":Data:150",
		("Grand Total Cashback") + ":Data:120",
		("Month-Year") + ":Data:100"
	]
	return columns

def get_linked(customer_company,filter_year):
	print customer_company
	print filter_year
	return frappe.db.sql("""SELECT SI.customer_name as Customer,  sum(SIT.base_net_amount) as Grand_Total_Cashback, YEAR(SI.posting_date),
CONCAT( MONTHNAME(SI.posting_date),"-",YEAR(SI.posting_date) ) AS Month_Year 
from `tabSales Invoice` as SI inner join `tabSales Invoice Item` as SIT ON SIT.parent = SI.name 
where 
SI.docstatus = 1 and 
YEAR(SI.posting_date)=%s and
SIT.item_name IN 
( SELECT parent from `tabItem Customer Detail` where customer_name = %s) group by SI.customer_name,SIT.base_net_amount, SIT.item_name, CONCAT( MONTHNAME(SI.posting_date),"-",YEAR(SI.posting_date) ) 
ORDER BY CONCAT( MONTHNAME(SI.posting_date),"-",YEAR(SI.posting_date) ) 
	""",(filter_year,customer_company), as_dict=1)

@frappe.whitelist()
def get_session_customer(useremail):
 	return frappe.db.sql("""select link_name as customer from `tabDynamic Link` where link_doctype="Customer" and parenttype="Contact" and parent in(
 select name from `tabContact` where user = %s)""" ,useremail, as_dict=1)

@frappe.whitelist()
def get_filter_year():
 	return frappe.db.sql("""select  distinct(YEAR(SI.posting_date)) as year from `tabSales Invoice` as SI
where SI.docstatus = 1 order by year desc""" ,as_dict=1)