from datetime import datetime

from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, select


class Subscriber(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def get_all_subscriber_emails(cls, session: Session) -> list[str]:
        result = session.exec(select(Subscriber.email))
        emails = result.all()
        return emails
