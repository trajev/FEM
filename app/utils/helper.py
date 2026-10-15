import string
import secrets


def generate_join_code(length: int = 10) -> str:
    """Generates a random uppercase alphanumeric string."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

