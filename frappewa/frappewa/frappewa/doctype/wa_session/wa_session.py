# Copyright (c) 2024, FrappeWA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WASession(Document):
    def before_save(self):
        # Validasi sederhana sebelum simpan
        if self.status == "Connected" and not self.phone_number:
            frappe.throw(_("Phone Number is required when status is Connected"))

    def on_update(self):
        # Log perubahan status jika berubah
        if self.has_value_changed("status"):
            frappe.db.sql("""
                INSERT INTO `tabWA Webhook Log` 
                (creation, modified, session, event_type, reference_doctype, reference_name) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (frappe.utils.now(), frappe.utils.now(), self.name, "status_change", "WASession", self.name))
