from langchain_core.tools import tool


@tool
def send_email(subject: str, content: str) -> None:
    """
    This function sends emails to users.
    """
    print('This is a email sending tool')
