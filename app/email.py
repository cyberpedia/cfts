from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List

from .config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_verification_email(email_to: str, username: str, token: str):
    """
    Sends a verification email to a new user.
    """
    # In a real app, the verification URL would point to your frontend.
    verification_url = f"http://localhost:8000/users/verify/{token}"

    html = f"""
    <html>
        <body>
            <h1>Hello, {username}!</h1>
            <p>Thank you for registering. Please click the link below to verify your email address:</p>
            <a href="{verification_url}">Verify Your Email</a>
            <p>If you did not register for this account, please ignore this email.</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="CTF Platform - Verify Your Email",
        recipients=[email_to],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        # In a production environment, you would log this error.
        print(f"Failed to send email: {e}")
