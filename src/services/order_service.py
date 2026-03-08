from src.utils.helpers import generate_order_id
from src.services.email_service import send_order_email


def process_order(name, phone, location, company):

    order_id = generate_order_id()

    order_details = {
        "order_id": order_id,
        "name": name,
        "phone": phone,
        "location": location,
        "company": company
    }

    send_order_email(order_details)

    return order_id