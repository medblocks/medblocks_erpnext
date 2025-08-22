app_name = "medblocks"
app_title = "Medblocks"
app_publisher = "Abhinand"
app_description = "Module to create tasks."
app_email = "abhinand@medblocks.org"
app_license = "MIT"
required_apps = ["healthcare"]
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/medblocks/css/medblocks.css"
# app_include_js = "/assets/medblocks/js/medblocks.js"
# include js, css files in header of web template
# web_include_css = "/assets/medblocks/css/medblocks.css"
# web_include_js = "/assets/medblocks/js/medblocks.js"
app_include_js = "aarthy.bundle.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "medblocks/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Invoice": "public/js/sales_invoice.js"}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "medblocks.utils.jinja_methods",
# 	"filters": "medblocks.utils.jinja_filters"
# }

# Installation
# ------------

before_install = "medblocks.setup.setup_Medblocks"
# after_install = "medblocks.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "medblocks.uninstall.before_uninstall"
# after_uninstall = "medblocks.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "medblocks.utils.before_app_install"
# after_app_install = "medblocks.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "medblocks.utils.before_app_uninstall"
# after_app_uninstall = "medblocks.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "medblocks.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }
override_doctype_class = {
	"Sales Invoice": "medblocks.medblocks.custom_doctype.sales_invoice.MedblocksSalesInvoice",
	"Item": "medblocks.medblocks.thirvusoft_customisations.utils.python.item.TSItem"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
   "Sales Invoice": {
		"on_submit": "medblocks.medblocks.utils.manage_invoice_submit_cancel",
		"on_cancel": "medblocks.medblocks.utils.manage_invoice_submit_cancel",
		"validate":"medblocks.medblocks.thirvusoft_customisations.utils.python.sales_invoice.check_batch_expiry_date"
	},
   "Payment Entry": {
		"on_submit": "medblocks.medblocks.utils.manage_payment_submit_cancel",
		"on_cancel": "medblocks.medblocks.utils.manage_payment_submit_cancel",
	},
	"Item": {
		"before_insert":"medblocks.medblocks.thirvusoft_customisations.utils.python.item.item_auto_series",
	},
	"Item Group": {
		"on_update":"medblocks.medblocks.thirvusoft_customisations.utils.python.item.validate_abbrivation",  
	}
}
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"medblocks.tasks.all"
# 	],
# 	"daily": [
# 		"medblocks.tasks.daily"
# 	],
# 	"hourly": [
# 		"medblocks.tasks.hourly"
# 	],
# 	"weekly": [
# 		"medblocks.tasks.weekly"
# 	],
# 	"monthly": [
# 		"medblocks.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "medblocks.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "medblocks.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "medblocks.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["medblocks.utils.before_request"]
# after_request = ["medblocks.utils.after_request"]

# Job Events
# ----------
# before_job = ["medblocks.utils.before_job"]
# after_job = ["medblocks.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"medblocks.auth.validate"
# ]
