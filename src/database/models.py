from datetime import datetime

from sqlmodel import Field, SQLModel


class Subscriber(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
