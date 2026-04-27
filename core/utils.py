import random
import string

def generate_short_code(length=6):
    """
    Generate a random short code for URLs
    Example: 'aB3xY9', 'Pq7Rt2', etc.
    """
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))