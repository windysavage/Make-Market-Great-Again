from langchain_core.tools import tool

from src.database.base import get_session
from src.database.models import Subscriber
from src.utils import send_email


@tool
def send_email_tool(subject: str, body: str) -> None:
    """
    Sends a plain-text email via SMTP.

    Args:
        subject (str): The subject line of the email.
        body (str): The plain-text body content of the email.
    """

    with get_session() as session:
        to_emails = Subscriber.get_all_subscriber_emails(session=session)

    return send_email(to_emails=to_emails, subject=subject, body=body)


if __name__ == '__main__':
    with get_session() as session:
        to_emails = Subscriber.get_all_subscriber_emails(session=session)
        send_email(to_emails=to_emails, subject='測試', body='測試用 body')
