# Copyright (c) 2024, FrappeWA and contributors
# For license information, please see license.txt

import frappe
from frappewa.frappewa.whatsapp_service import WhatsAppService

def send_message_job(message_id, session_name, phone_number, message, media_url=None):
    """
    Background Job untuk mengirim pesan secara asynchronous.
    Fungsi ini akan dipanggil oleh worker Frappe.
    """
    try:
        # Update status jadi Sending
        msg_doc = frappe.get_doc("WAMessage", message_id)
        msg_doc.status = "Sending"
        msg_doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Inisialisasi service
        service = WhatsAppService(session_name)
        
        # LOGIKA UTAMA PENGIRIMAN ADA DI SINI
        # Karena whatsapp-web.js berbasis Node, kita punya 2 opsi:
        # 1. Panggil script Node kecil via subprocess yang melakukan pengiriman
        # 2. Kirim request HTTP ke service Node yang berjalan terpisah (disarankan)
        
        # Simulasi pemanggilan ke Node Service (Opsi 2 - Disarankan)
        # Dalam implementasi nyata, ganti URL ini dengan endpoint service Node Anda
        node_service_url = frappe.db.get_single_value("WA Settings", "node_service_url")
        
        if not node_service_url:
            raise Exception("Node Service URL not configured in WA Settings")

        import requests
        payload = {
            "session": session_name,
            "to": phone_number,
            "body": message
        }
        if media_url:
            payload["media"] = media_url
            
        response = requests.post(f"{node_service_url}/send", json=payload, timeout=10)
        
        if response.status_code == 200:
            msg_doc.status = "Sent"
            msg_doc.response_data = response.text
        else:
            msg_doc.status = "Error"
            msg_doc.error_log = f"Node service error: {response.text}"
            
        msg_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "WhatsApp Send Message Error")
        if frappe.db.exists("WAMessage", message_id):
            msg_doc = frappe.get_doc("WAMessage", message_id)
            msg_doc.status = "Error"
            msg_doc.error_log = str(e)
            msg_doc.save(ignore_permissions=True)
            frappe.db.commit()

@frappe.whitelist()
def handle_incoming_message(session_name, from_number, message_body, timestamp=None):
    """
    Webhook handler untuk pesan masuk dari Node Service.
    Dipanggil oleh service Node ketika ada pesan masuk dari WhatsApp.
    """
    try:
        doc = frappe.get_doc({
            "doctype": "WAMessage",
            "session": session_name,
            "phone_number": from_number,
            "message": message_body,
            "type": "Incoming",
            "status": "Received",
            "timestamp": timestamp or frappe.utils.now()
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        # Trigger Webhook User jika dikonfigurasi
        trigger_user_webhooks(session_name, "message_received", doc.as_dict())
        
        return {"status": "success", "message_id": doc.name}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "WhatsApp Incoming Message Error")
        return {"status": "error", "message": str(e)}

def trigger_user_webhooks(session_name, event, data):
    """Memicu webhook yang dikonfigurasi user"""
    session_doc = frappe.get_doc("WASession", session_name)
    
    # Cek apakah webhook diaktifkan di sesi ini
    if not session_doc.enable_webhook:
        return
        
    webhook_url = session_doc.webhook_url
    if not webhook_url:
        return
        
    import requests
    try:
        payload = {
            "event": event,
            "session": session_name,
            "data": data
        }
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Webhook Trigger Failed")

@frappe.whitelist()
def cleanup_old_sessions():
    """Daily scheduler job untuk cleanup sesi lama"""
    from datetime import timedelta
    cutoff_date = frappe.utils.add_days(frappe.utils.nowdate(), -30)
    
    sessions = frappe.get_all("WASession", 
                             filters={"modified": ["<", cutoff_date], "status": "Disconnected"},
                             fields=["name"])
    
    for session in sessions:
        frappe.delete_doc("WASession", session.name, ignore_permissions=True)
    
    frappe.db.commit()
    return f"Cleaned up {len(sessions)} old sessions"

@frappe.whitelist()
def cleanup_old_messages():
    """Daily scheduler job untuk cleanup pesan lama"""
    from datetime import timedelta
    retention_days = frappe.db.get_single_value("WA Settings", "message_retention_days") or 90
    cutoff_date = frappe.utils.add_days(frappe.utils.nowdate(), -retention_days)
    
    messages = frappe.get_all("WAMessage", 
                             filters={"timestamp": ["<", cutoff_date]},
                             fields=["name"])
    
    for message in messages:
        frappe.delete_doc("WAMessage", message.name, ignore_permissions=True)
    
    frappe.db.commit()
    return f"Cleaned up {len(messages)} old messages"
