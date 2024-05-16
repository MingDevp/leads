import emails
import logging

from app import config
from dataclasses import dataclass
from jinja2 import Template
from pathlib import Path
from typing import Any


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def generate_new_lead_email(first_name: str, last_name: str) -> EmailData:
    subject = f"New lead for user {first_name}, {last_name}"
    html_content = render_email_template(
        template_name="new_lead.html",
        context={
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def send_email(
    *,
    email_to: list[str],
    subject: str = "",
    html_content: str = "",
) -> None:
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(config.EMAILS_FROM_NAME, config.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": config.SMTP_HOST, "port": config.SMTP_PORT}
    if config.SMTP_TLS:
        smtp_options["tls"] = True
    elif config.SMTP_SSL:
        smtp_options["ssl"] = True
    if config.SMTP_USER:
        smtp_options["user"] = config.SMTP_USER
    if config.SMTP_PASSWORD:
        smtp_options["password"] = config.SMTP_PASSWORD

    for e in email_to:
        response = message.send(to=e, smtp=smtp_options)
        logging.info(f"send email result: {response}")
