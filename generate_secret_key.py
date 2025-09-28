#!/usr/bin/env python
"""
Generate a secure Django SECRET_KEY for production use.
"""
import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key."""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print("Generated Django SECRET_KEY:")
    print(f"SECRET_KEY={secret_key}")
    print("\nCopy this to your .env.production file!")