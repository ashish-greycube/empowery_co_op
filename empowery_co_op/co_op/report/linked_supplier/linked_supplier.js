// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Linked Supplier"] = {
	"filters": [{
		"fieldname": "customer",
		"label": __("Customer"),
		"fieldtype": "Link",
		"options": "Customer",
		"read_only": 1
	}, ],
	onload: (report) => {
		get_session_customer();

		function get_session_customer() {
			frappe.call({
				method: "empowery_co_op.co_op.report.linked_supplier.linked_supplier.get_session_customer",
				args: {
					useremail: frappe.session.user_email
				},
				callback: function (data) {
					frappe.query_report_filters_by_name.customer.set_input(data.message[0].link_name);
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