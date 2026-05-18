# Copyright (c) 2024, FrappeWA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WASettings(Document):
    def validate(self):
        # Validasi konfigurasi
        if self.default_retry_count < 0:
            frappe.throw(_("Retry count cannot be negative"))
