# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = get_columns(), get_data()
	return columns, data

def get_columns():
	columns = [
		("Supplier") + ":Link/Supplier:270",
		("# of Linked Customer") + ":Data:150",
		("% of Engagement") + ":Data:150"
	]
	return columns

def get_data():
	data = frappe.db.sql("""
		select concat('<a href="desk#query-report/Customer%20Engagement?supplier=',supp.name,'">',supp.name,'</a>') as 'Supplier',
				concat('<a href="desk#query-report/Customer%20Engagement?supplier=',supp.name,'">',cust_link.linked,'</a>')as '# of Linked Customer',
				concat('<a href="desk#query-report/Customer%20Engagement?supplier=',supp.name,'">',ROUND(cust_link.linked/(select count(customer_name) from `tabCustomer` where docstatus=0 and customer_group != 'Supplier')*100,2),'</a>')as '% of Engagement'
    	from tabSupplier supp
    		left outer join (
    			select parent,count(*) linked from `tabDynamic Link` 
    			where link_doctype='Customer' and parenttype='Supplier'and docstatus = 0 and parentfield='links' 
    			group by parent) cust_link on cust_link.parent = supp.name
    			where supp.docstatus=0 and supp.disabled!=1""", as_dict=1)
		
	return data
@frappe.whitelist()
def get_color_codes():
	color_codes={}
	color_codes['color_1']=frappe.db.get_single_value('Supplier Engagement Report Settings', 'color_1')
	color_codes['red_start']=frappe.db.get_single_value('Supplier Engagement Report Settings', 'red_zone_start_value')
	color_codes['color_2']=frappe.db.get_single_value('Supplier Engagement Report Settings', 'color_2')
	color_codes['yellow_start']=frappe.db.get_single_value('Supplier Engagement Report Settings', 'yellow_zone_start_value')
	color_codes['yellow_end']=frappe.db.get_single_value('Supplier Engagement Report Settings', 'yellow_zone_end_value')
	color_codes['color_3']=frappe.db.get_single_value('Supplier Engagement Report Settings', 'color_3')
	color_codes['green_end']=frappe.db.get_single_value('Supplier Engagement Report Settings', 'green_zone_end_value')
	return color_codes