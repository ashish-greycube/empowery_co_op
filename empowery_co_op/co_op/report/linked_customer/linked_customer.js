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
	}, ],
	onload: (report) => {
		get_session_supplier();

		function get_session_supplier() {

			frappe.call({
				method: "empowery_co_op.co_op.report.linked_customer.linked_customer.get_session_supplier",

				args: {
					useremail: frappe.session.user_email
				},
				callback: function (data) {
					frappe.query_report_filters_by_name.supplier.set_input(data.message[0].link_name);

				}
			})
		}
	},
}