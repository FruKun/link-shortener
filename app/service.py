import random

import validators

from app import database
from app.model import Url
from app.settings import Config

from . import errors


def generate_short_url(symbols: list[str] = Config.SYMBOLS, length: int = 4) -> str:
    new_url = ""
    for length in range(length, 120):
        flag = False
        # чтобы сильно не увеличивать время запроса при большом заполнении бд
        for j in range(0, 10):
            new_url = "".join(random.choices(symbols, k=length))
            if Url.query.filter_by(short_url=new_url).count() != 0:
                continue
            else:
                flag = True
                break
        if flag:
            break
    return new_url


def validate_short_url(url: str | None) -> str:
    if url is None or url == "":
        return generate_short_url()
    elif not isinstance(url, str):
        return validate_short_url(str(url))
    else:
        if not set(Config.SYMBOLS).issuperset(url):
            raise errors.ValidationError
        if Url.query.filter_by(short_url=url).count() != 0:
            raise errors.IntegrityError
        return url


def validate_original_url(original_url: str) -> str:
    validators.url(original_url, r_ve=True)
    return original_url


def update_count(url: Url) -> None:
    url.count += 1
    database.session.commit()
