import smtplib
from email.message import EmailMessage
# import app.services.order as order
from backend.routes import orders
from fastapi import background, logger
from sqlalchemy.sql.functions import user
def send_email_smtp(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "no-reply@tayyab.com"
    msg["To"] = to_email
    msg.set_content(body)
    # Example using local SMTP / or configure SMTP in settings
    with smtplib.SMTP("localhost") as s:
        s.send_message(msg)

# Enhanced email service with templates
async def send_order_confirmation(user_email: str, order_id: int, order_details: dict):
    subject = f"🎉 Order Confirmed - #{order_id}"
    body = f"""
    Dear Customer,

    Your jewellery order #{order_id} has been confirmed!

    Items: {len(order_details['items'])}
    Total: Rs. {order_details['total_price']:,.2f}

    Thank you for choosing Tayyab Jewellers!
    """
    await send_email_smtp(user_email, subject, body)


def send_order_status_email(user_email: str, order_id: int, status: str, additional_info: str = ""):
    """Send email when order status changes"""
    subject = f"Order #{order_id} Status Update"

    status_messages = {
        "processing": "is being processed",
        "shipped": "has been shipped",
        "delivered": "has been delivered",
        "cancelled": "has been cancelled"
    }

    status_message = status_messages.get(status, "status has been updated")

    body = f"""
    Dear Customer,

    Your order #{order_id} {status_message}.

    {additional_info}

    Thank you for choosing Tayyab Jewellers!

    Best regards,
    Tayyab Jewellers Team
    """
    send_email_smtp(user_email, subject, body)