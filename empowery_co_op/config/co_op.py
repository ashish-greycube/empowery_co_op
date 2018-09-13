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
			"label": _("Ven-Powery"),
			"icon": "fa fa-print",
			"items": [
				{
					"type": "doctype",
					"name": "Service Category",
					"label": _("Vendor Service Category"),
					"description": _("Define Service Category"),
					"hide_count": False
				},
				{
					"type": "doctype",
					"name": "Vendor Carousel and Email template",
					"label": _("Vendor Carousel & Email template"),
					"description": _("Define Vendor Carousel & Offer email"),
					"hide_count": True
				},				
				{
					"type": "doctype",
					"name": "Supplier",
					"label": _("Vendor listing Settings & Content"),
					"description": _("Define Vendor Offer meta & content"),
					"hide_count": True
				}
			]
		}
    ]