import secrets

ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
SECRET_KEY: str = secrets.token_urlsafe(32)

LAWYER_EMAIL: str
EMAILS_FROM_EMAIL: str | None = None
EMAILS_FROM_NAME: str | None = None
SMTP_TLS: bool = True
SMTP_SSL: bool = False
SMTP_PORT: int = 587
SMTP_HOST: str | None = None
SMTP_USER: str | None = None
SMTP_PASSWORD: str | None = None
