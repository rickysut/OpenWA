# Copyright (c) 2024, FrappeWA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WAMessage(Document):
    def before_insert(self):
        # Auto set timestamp jika belum ada
        if not self.timestamp:
            self.timestamp = frappe.utils.now()

    def validate(self):
        # Validasi nomor telepon sederhana
        if self.phone_number and not self.phone_number.startswith("+"):
            # Bisa ditambahkan logika format nomor di sini
            pass
