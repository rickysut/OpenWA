# Copyright (c) 2024, FrappeWA and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import subprocess
import json
import os

class WhatsAppService:
    def __init__(self, session_name):
        self.session_name = session_name
        self.session_doc = frappe.get_doc("WASession", session_name)
        
    def start_client(self):
        """Memulai klien WhatsApp (Node.js)"""
        if not self.session_doc.node_script_path:
            frappe.throw(_("Node script path not configured in Session"))
            
        # Memproses script Node.js sebagai subprocess
        # Dalam produksi, ini sebaiknya dikelola oleh Process Manager terpisah
        try:
            cmd = ["node", self.session_doc.node_script_path, self.session_name]
            # Menyimpan PID jika perlu dimonitor
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.session_doc.pid = process.pid
            self.session_doc.status = "Connecting"
            self.session_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "started", "pid": process.pid}
        except Exception as e:
            self.session_doc.status = "Error"
            self.session_doc.error_log = str(e)
            self.session_doc.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.throw(_("Failed to start client: {0}").format(str(e)))

    def stop_client(self):
        """Menghentikan klien WhatsApp"""
        if self.session_doc.pid:
            try:
                os.kill(self.session_doc.pid, 9) # SIGKILL
                self.session_doc.status = "Disconnected"
                self.session_doc.pid = None
                self.session_doc.save(ignore_permissions=True)
                frappe.db.commit()
                return {"status": "stopped"}
            except Exception as e:
                frappe.throw(_("Failed to stop client: {0}").format(str(e)))
        else:
            self.session_doc.status = "Disconnected"
            self.session_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "already_stopped"}

    @staticmethod
    @frappe.whitelist()
    def send_message(session_name, phone_number, message, media_url=None):
        """
        API Whitelisted untuk mengirim pesan.
        Bisa dipanggil dari Dashboard atau API Eksternal.
        """
        doc = frappe.get_doc("WASession", session_name)
        if doc.status != "Connected":
            frappe.throw(_("Session is not connected. Current status: {0}").format(doc.status))

        # Membuat record pesan keluar
        msg_doc = frappe.get_doc({
            "doctype": "WAMessage",
            "session": session_name,
            "phone_number": phone_number,
            "message": message,
            "media_url": media_url,
            "type": "Outgoing",
            "status": "Pending"
        })
        msg_doc.insert(ignore_permissions=True)
        
        # Antrikan ke background job agar tidak blocking
        frappe.enqueue(
            "frappewa.frappewa.api.send_message_job",
            queue="long",
            message_id=msg_doc.name,
            session_name=session_name,
            phone_number=phone_number,
            message=message,
            media_url=media_url
        )
        
        return {"message_id": msg_doc.name, "status": "queued"}

@frappe.whitelist()
def get_qr_code(session_name):
    """Mengambil QR Code terbaru untuk sesi tertentu"""
    # Asumsi QR code disimpan di field custom atau file attachment
    doc = frappe.get_doc("WASession", session_name)
    if doc.qr_code_image:
        return {"qr_code": doc.qr_code_image}
    return {"qr_code": None, "message": "No QR code available yet"}
