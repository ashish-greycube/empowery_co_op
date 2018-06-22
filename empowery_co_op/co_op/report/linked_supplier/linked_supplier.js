// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Linked Supplier"] = {
	"filters": [{
		"fieldname": "customer",
		"label": __("Customer"),
		"fieldtype": "Select",
		"options": "Customer"
		
	},


],
	onload: (report) => {
		report.page.add_inner_button(__("Back to Portal"), function() {
			location.href = 'me'
		});
		
		get_session_customer();

		function get_session_customer() {
			frappe.call({
				method: "empowery_co_op.co_op.report.linked_supplier.linked_supplier.get_session_customer",
				args: {
					useremail: frappe.session.user_email
				},
				callback: function (data) {
					if (data.message != undefined){
					var filter = frappe.query_report_filters_by_name.customer
					var option_values=[];
					data.message.forEach(element => {
						option_values.push(element.link_name);
						
					});
					filter.df.options=option_values
					filter.set_input(option_values[0]);
					filter.refresh();	
				}
				else{
					var filter = frappe.query_report_filters_by_name.customer
					filter.df.read_only=1;
					filter.refresh();
					frappe.msgprint("Login user is not a valid empowery customer")
				}				
				}
			})
		}

		frappe.add_party_link = function (custname, suppname, isLinked) {
			frappe.call({
				method: "empowery_co_op.co_op.report.linked_supplier.linked_supplier.add_party_link",
				args: {
					custname: custname,
					suppname: suppname,
					isLinked: isLinked

				},
				callback: function (data) {
					frappe.click_button("Refresh")
				}
			})
		}
		frappe.remove_party_link = function (custname, suppname) {
			frappe.call({

				method: "empowery_co_op.co_op.report.linked_supplier.linked_supplier.remove_party_link",
				args: {
					custname: custname,
					suppname: suppname

				},
				callback: function (data) {
					frappe.click_button("Refresh")

				}
			})
		}

	},
}

