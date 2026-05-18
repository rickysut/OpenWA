# Copyright (c) 2024, FrappeWA and contributors
# For license information, please see license.txt

import frappe

def before_install():
    pass

def after_install():
    """Jalankan setelah aplikasi diinstall"""
    create_default_settings()
    create_default_roles()

def before_uninstall():
    pass

def create_default_settings():
    """Membuat dokumen WA Settings default jika belum ada"""
    if not frappe.db.exists("WA Settings"):
        settings = frappe.get_doc({
            "doctype": "WA Settings",
            "enable_logging": 1,
            "default_retry_count": 3
        })
        settings.insert(ignore_permissions=True)
        frappe.db.commit()

def create_default_roles():
    """Membuat role khusus untuk WhatsApp Manager"""
    roles = ["WhatsApp Manager", "WhatsApp User"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)
    frappe.db.commit()

def get_permission_query_conditions(user):
    return None
