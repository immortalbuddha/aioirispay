import string
import random

def generate_invoice_id(size: int = 15) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    