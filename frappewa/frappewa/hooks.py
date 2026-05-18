app_name = "frappewa"
app_title = "FrappeWA"
app_publisher = "FrappeWA Team"
app_description = "WhatsApp Integration Module for Frappe Framework"
app_email = "hello@frappewa.com"
app_license = "MIT"

required_apps = ["frappe"]

before_install = "frappewa.frappewa.utils.before_install"
after_install = "frappewa.frappewa.utils.after_install"

scheduler_events = {
    "daily": [
        "frappewa.frappewa.api.cleanup_old_sessions",
        "frappewa.frappewa.api.cleanup_old_messages"
    ]
}

permission_query_conditions = {
    "WASession": "frappewa.frappewa.utils.get_permission_query_conditions",
    "WAMessage": "frappewa.frappewa.utils.get_permission_query_conditions"
}

doc_events = {
    "WASession": {
        "on_update": "frappewa.frappewa.doctype.wa_session.wa_session.on_update"
    }
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappewa/css/frappewa.css"
# app_include_js = "/assets/frappewa/js/frappewa.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappewa/css/frappewa.css"
# web_include_js = "/assets/frappewa/js/frappewa.js"

# include custom scss in every website theme (without signing in)
# website_theme_scss = "frappewa/public/scss/website"

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

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for Website Records
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "frappewa.frappewa.jinja_methods",
# 	"filters": "frappewa.frappewa.jinja_filters"
# }

# Installation
# ------------

# before_install = "frappewa.install.before_install"
# after_install = "frappewa.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "frappewa.uninstall.before_uninstall"
# after_uninstall = "frappewa.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the App being installed is treated as the key
# your_integration_name: {
# 	"hooks": {
# 		"before_app_first_install": [
# 			"frappewa.your_integration_name.before_app_first_install"
# 		],
# 		"after_app_install": [
# 			"frappewa.your_integration_name.after_app_install"
# 		],
# 	]
# }

# App Hooks
# ---------

# Before inserting a new doc
# doc_events = {
# 	"*": {
# 		"before_insert": "frappewa.frappewa.utils.before_insert"
# 	}
# }

# Permissions
# -----------
# Permissions evaluated in sandbox mode.
# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions"
# }
#
# Has Permission
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission"
# }

# DocType Class
# ---------------
# Override standard doctype classes
# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
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
# 		"frappewa.tasks.all"
# 	],
# 	"daily": [
# 		"frappewa.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappewa.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappewa.tasks.weekly"
# 	],
# 	"monthly": [
# 		"frappewa.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "frappewa.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappewa.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# it is generated from the request JSON
#
# whitelisted_paths = {
# 	"/api/method/frappewa.method1": "frappewa.method1",
# 	"/api/method/frappewa.method2": "frappewa.method2"
# }

#
# ignoring_link_doctypes = [
# 	("DocType", "DocType"),
# 	("DocType", "DocType"),
# ]
#
# fixtures = ["Custom Field", "Property Setter"]

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["frappewa.utils.before_request"]
# after_request = ["frappewa.utils.after_request"]

# Job Events
# ----------
# before_job = ["frappewa.utils.before_job"]
# after_job = ["frappewa.utils.after_job"]

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
# 	"frappewa.auth.validate"
# ]

# Automatically update python controller properties with specified fields
# auto_name_adoption = {
# 	"MyDocType": "naming_field"
# }
