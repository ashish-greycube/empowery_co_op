from frappe import _

def get_data():
	return [
		{
			"label": _("Empowery co-op admin facility"),
			"icon": "fa fa-print",
			"items": [
				{
					"type": "report",
					"name": "Supplier Engagement",
					"is_query_report": True,
					"route": "query-report/Supplier Engagement",
					"description": _("Supplier Engagement Report.")
				},
				{
					"type": "doctype",
					"name": "Supplier Engagement Report Settings",
					"label": _("Supplier Engagement color settings"),
					"description": _("Set Default Color Values"),
					"hide_count": True
				}
			]
		},
		{
			"label": _("Empowery co-op member facility"),
			"icon": "fa fa-print",
			"items": [
				{
					"type": "report",
					"name": "Linked Customer",
					"is_query_report": True,
					"route": "query-report/Linked Customer",
					"label": _("Supplier report to check its linked customer"),
					"description": _("Report for supplier to check linked customer.")
				},
				{
					"type": "report",
					"name": "Linked Supplier",
					"is_query_report": True,
					"route": "query-report/Linked Supplier",
					"label": _("Customer report to check its linked supplier"),
					"description": _("Report for customer to check linked supplier.")
				},
			]
		},
    ]