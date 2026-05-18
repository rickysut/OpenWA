# Copyright (c) 2024, FrappeWA Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def send_message(session_name, phone, message, media_url=None):
    """
    Send WhatsApp message via session
    
    Args:
        session_name: Name of the WA Session
        phone: Phone number (with country code)
        message: Text message to send
        media_url: Optional URL of media file
    
    Returns:
        dict: Status of message sending
    """
    try:
        # Get session document
        session = frappe.get_doc("WA Session", session_name)
        
        if session.status != "Connected":
            frappe.throw(_("Session is not connected"))
        
        # TODO: Implement actual WhatsApp message sending via whatsapp-web.js
        # This will be handled by a background job or external service
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Message queued for sending")
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Send Message Error"))
        frappe.throw(str(e))


@frappe.whitelist()
def get_qr_code(session_name):
    """
    Get QR Code for WhatsApp session authentication
    
    Args:
        session_name: Name of the WA Session
    
    Returns:
        dict: QR Code data
    """
    try:
        session = frappe.get_doc("WA Session", session_name)
        
        if session.status == "Connected":
            return {
                "success": False,
                "message": _("Session already connected")
            }
        
        # Update status to QR Code Pending
        session.status = "QR Code Pending"
        session.save(ignore_permissions=True)
        
        # TODO: Generate QR code via whatsapp-web.js
        # This will trigger the WhatsApp client to generate QR
        
        return {
            "success": True,
            "qr_code": session.qr_code,
            "message": _("QR code generated. Please scan with WhatsApp.")
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Get QR Code Error"))
        frappe.throw(str(e))


@frappe.whitelist()
def connect_session(session_name):
    """
    Connect/Initialize WhatsApp session
    
    Args:
        session_name: Name of the WA Session
    
    Returns:
        dict: Connection status
    """
    try:
        session = frappe.get_doc("WA Session", session_name)
        
        if session.status == "Connected":
            return {
                "success": False,
                "message": _("Session already connected")
            }
        
        # Update status to Connecting
        session.status = "Connecting"
        session.save(ignore_permissions=True)
        
        # TODO: Initialize whatsapp-web.js client
        # This will be done via background job or Node.js service
        
        return {
            "success": True,
            "message": _("Connection initiated. Please get QR code.")
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Connect Session Error"))
        frappe.throw(str(e))


@frappe.whitelist()
def disconnect_session(session_name):
    """
    Disconnect WhatsApp session
    
    Args:
        session_name: Name of the WA Session
    
    Returns:
        dict: Disconnection status
    """
    try:
        session = frappe.get_doc("WA Session", session_name)
        
        if session.status == "Disconnected":
            return {
                "success": False,
                "message": _("Session already disconnected")
            }
        
        # Update status
        session.status = "Disconnected"
        session.phone_number = None
        session.qr_code = None
        session.save(ignore_permissions=True)
        
        # TODO: Cleanup whatsapp-web.js client
        
        return {
            "success": True,
            "message": _("Session disconnected")
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Disconnect Session Error"))
        frappe.throw(str(e))
