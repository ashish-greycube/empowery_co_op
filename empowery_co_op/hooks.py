# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "empowery_co_op"
app_title = "CO-OP"
app_publisher = "GreyCube Technologies"
app_description = "Empowery co-op membership program"
app_icon = "octicon octicon-organization"
app_color = "#f25e94"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/empowery_co_op/css/empowery_co_op.css"
# app_include_js = "/assets/empowery_co_op/js/empowery_co_op.js"

# include js, css files in header of web template
# web_include_css = "/assets/empowery_co_op/css/empowery_co_op.css"
# web_include_js = "/assets/empowery_co_op/js/empowery_co_op.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"
# on_session_creation = "empowery_co_op.api.set_portal_homepage"
# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

web_include_css = [
    "/assets/frappe/js/lib/slickgrid/slick.grid.css",
    "/assets/frappe/js/lib/slickgrid/slick-default-theme.css",
    "/assets/frappe/css/slickgrid.css"
]

web_include_js = [
    "/assets/frappe/js/lib/slickgrid/jquery.event.drag.js",
    "/assets/frappe/js/lib/slickgrid/plugins/slick.cellrangedecorator.js",
    "/assets/frappe/js/lib/slickgrid/plugins/slick.cellrangeselector.js",
    "/assets/frappe/js/lib/slickgrid/plugins/slick.cellselectionmodel.js",
    "/assets/frappe/js/lib/slickgrid/plugins/slick.cellexternalcopymanager.js",
    "/assets/frappe/js/lib/slickgrid/slick.core.js",
    "/assets/frappe/js/lib/slickgrid/slick.grid.js",
    "/assets/frappe/js/lib/slickgrid/slick.formatters.js",
    "/assets/frappe/js/lib/slickgrid/slick.dataview.js"

]

# Website user home page (by function)
# get_website_user_home_page = "empowery_co_op.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "empowery_co_op.install.before_install"
# after_install = "empowery_co_op.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "empowery_co_op.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"empowery_co_op.tasks.all"
# 	],
# 	"daily": [
# 		"empowery_co_op.tasks.daily"
# 	],
# 	"hourly": [
# 		"empowery_co_op.tasks.hourly"
# 	],
# 	"weekly": [
# 		"empowery_co_op.tasks.weekly"
# 	]
# 	"monthly": [
# 		"empowery_co_op.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "empowery_co_op.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "empowery_co_op.event.get_events"
# }

fixtures = [
    	{
		"dt":"Custom Script",
		"filters":[
			["name", "in", [
			"Supplier-Client","Customer-Client","Supplier Engagement Report Settings-Client"]],
		]
	},

]