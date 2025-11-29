from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
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

async def send_verification_email(email: str, token: str):
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Please use the following token to verify your email: {token}",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
