from langchain_core.tools import tool

from src.utils import send_email


@tool
def send_email_tool(to_email: str, subject: str, body: str) -> None:
    """
    This tool can send emails to users.
    """
    return send_email(to_email=to_email, subject=subject, body=body)
