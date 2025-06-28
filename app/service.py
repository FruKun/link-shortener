import random

from app.database import database
from app.model import Url
from app.settings import Config


def generate_short_url(length: int = 6) -> str:
    return "".join(random.choices(Config.SYMBOLS, k=length))


def update_count(url: Url) -> None:
    url.count += 1
    database.session.commit()
