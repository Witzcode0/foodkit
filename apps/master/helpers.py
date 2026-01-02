import re
import string
import random

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def is_valid_mobile(number):
    pattern = r'^\+91\s[6-9]\d{9}$'
    return bool(re.match(pattern, number))

def is_valid_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))

def is_valid_password(password):
    missing = []

    if len(password) < 8:
        missing.append("minimum 8 characters")

    if not any(c.islower() for c in password):
        missing.append("one lowercase letter")

    if not any(c.isupper() for c in password):
        missing.append("one uppercase letter")

    if not any(c.isdigit() for c in password):
        missing.append("one digit")

    if not any(c in string.punctuation for c in password):
        missing.append("one special symbol")

    if missing:
        return False, "Password must contain " + ", ".join(missing)
    
    return True, "Password is valid"


def generate_otp(length=6):
    """
    Generate numeric OTP of given length (4 or 6)
    """
    if length not in (4, 6):
        raise ValueError("OTP length must be 4 or 6")

    return ''.join(random.choice(string.digits) for _ in range(length))