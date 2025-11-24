# app/utils/hashing.py
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Create a PasswordHasher instance
ph = PasswordHasher()

# Hash a password
def hash_password(password: str) -> str:
    return ph.hash(password)

# Verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
