# Copyright (c) 2024, FrappeWA Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def send_whatsapp_message(session_name, phone_number, message, media_url=None, media_type="None"):
    """
    Send WhatsApp message and create WA Message record
    
    Args:
        session_name: WA Session name
        phone_number: Recipient phone number
        message: Message text
        media_url: Optional media URL
        media_type: Type of media (None, Image, Video, Document, Audio)
    
    Returns:
        dict: Status with message ID
    """
    try:
        # Create message record
        msg_doc = frappe.get_doc({
            "doctype": "WA Message",
            "session": session_name,
            "message_type": "Outgoing",
            "phone_number": phone_number,
            "message": message,
            "media_url": media_url,
            "media_type": media_type,
            "status": "Pending"
        })
        msg_doc.insert(ignore_permissions=True)
        
        # Call API to send message
        from frappewa.api.session import send_message
        result = send_message(session_name, phone_number, message, media_url)
        
        # Update status
        msg_doc.status = "Sent"
        msg_doc.save(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message_id": msg_doc.name,
            "status": "Sent"
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Send WhatsApp Message Error"))
        frappe.throw(str(e))
