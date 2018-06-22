// Copyright (c) 2016, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Engagement"] = {
	"filters": [{
		"fieldname": "supplier",
		"label": __("Supplier"),
		"fieldtype": "Link",
		"options": "Supplier"}

	],
	onload: (report) => {
		report.page.add_inner_button(__("Back to Supplier Engagement"), function() {
			frappe.set_route('query-report', 'Supplier Engagement', {});
		});

	frappe.add_party_link = function (custname, suppname, isLinked) {
		frappe.call({
			method: "empowery_co_op.co_op.report.customer_engagement.customer_engagement.add_party_link",
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

			method: "empowery_co_op.co_op.report.customer_engagement.customer_engagement.remove_party_link",
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
