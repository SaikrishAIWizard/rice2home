import uuid

def generate_order_id():
    return str(uuid.uuid4())[:8].upper()