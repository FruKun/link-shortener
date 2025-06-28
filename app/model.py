from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app import database


class Url(database.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str]
    short_url: Mapped[str] = mapped_column(unique=True)
    count: Mapped[int] = mapped_column(default=0)
    last_use: Mapped[datetime] = mapped_column(onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def update_count(self) -> None:
        self.count += 1
