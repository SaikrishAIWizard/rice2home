import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config.settings import EMAIL_USER, EMAIL_PASS, EMAIL_TO


def send_order_email(order_details: dict):
    """
    Sends rice order details via Gmail SMTP
    """

    # Email subject
    subject = f"New Rice Order - {order_details['order_id']}"

    # Email body
    body = f"""
New Rice Order Received

Order ID: {order_details['order_id']}

Customer Details
-----------------------
Name: {order_details['name']}
Phone: {order_details['phone']}

Rice Brand
-----------------------
{order_details['company']}

Delivery Location
-----------------------
{order_details['location']}

Google Maps:
https://www.google.com/maps?q={order_details['location']}

--------------------------------
This order was generated from Rice Order App
"""

    # Create email
    msg = MIMEMultipart()

    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    # Attach body
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(EMAIL_USER, EMAIL_PASS)

            server.send_message(msg)

        print("Order email sent successfully")

    except Exception as e:
        print("Email sending failed:", e)