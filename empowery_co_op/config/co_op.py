from frappe import _

def get_data():
	return [
		{
			"label": _("Empowery CO-OP"),
			"items": [
				{
					"type": "report",
					"name": "Linked Customer",
				},
				{
					"type": "report",
					"name": "Linked Supplier",
				}
			]
		}
    ]
