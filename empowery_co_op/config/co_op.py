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
		}
    ]