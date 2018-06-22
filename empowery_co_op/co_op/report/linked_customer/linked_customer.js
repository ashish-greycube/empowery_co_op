// Copyright (c) 2016, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Linked Customer"] = {
	"filters": [{
		"fieldname": "supplier",
		"label": __("Supplier"),
		"fieldtype": "Link",
		"options": "Supplier",
		"read_only": 1,
	}
],
	onload: (report) => {
		report.page.add_inner_button(__("Back to Portal"), function() {
			location.href = 'me'
		});

	

		get_session_supplier();

		function get_session_supplier() {

			frappe.call({
				method: "empowery_co_op.co_op.report.linked_customer.linked_customer.get_session_supplier",

				args: {
					useremail: frappe.session.user_email
				},
				callback: function (data) {
					console.log(data)
					if (data.message != undefined){
					frappe.query_report_filters_by_name.supplier.set_input(data.message[0].link_name);}
					else{
						frappe.msgprint("Login user is not a valid empowery supplier")
						frappe.query_report_filters_by_name.supplier.set_input("");
						filter.refresh();
					}

				}
			})
		}
	},
}