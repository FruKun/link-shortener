import random

from pydantic import AnyUrl

from app.database import database
from app.model import Url
from app.settings import Config

from . import errors


def generate_short_url(length: int = 6) -> str:
    new_url = "".join(random.choices(Config.SYMBOLS, k=length))
    if database.session.execute(
        database.select(Url).filter_by(short_url=new_url)
    ).first():
        generate_short_url()
    return new_url


def validate_short_url(url: str | None) -> str:
    if url is None or url == "":
        return generate_short_url()
    else:
        if not set(Config.SYMBOLS).issuperset(url):
            raise errors.ValidationError
        if database.session.execute(
            database.select(Url).filter_by(short_url=url)
        ).first():
            raise errors.IntegrityError
        return url


def validate_original_url(url: str) -> str:
    AnyUrl(url)
    return url


def update_count(url: Url) -> None:
    url.count += 1
    database.session.commit()
