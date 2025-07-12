from langchain_core.tools import tool

from src.utils import send_email


@tool
def send_email_tool(to_email: str, subject: str, body: str) -> None:
    """
    Sends a plain-text email via SMTP.

    Args:
        to_email (str): The recipient's email address.
        subject (str): The subject line of the email.
        body (str): The plain-text body content of the email.
    """
    return send_email(to_email=to_email, subject=subject, body=body)
