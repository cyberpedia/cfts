import secrets
from passlib.context import CryptContext

# Setup password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def generate_verification_token() -> str:
    """
    Generates a secure, URL-safe token for email verification.
    """
    return secrets.token_urlsafe(32)
