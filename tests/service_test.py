import pytest
from sqlalchemy import func

from app import Config, database
from app.model import Url
from app.service import generate_short_url


@pytest.mark.parametrize(
    "symbols, length",
    [
        (["1", "2"], 2),
        (["1", "2"], 10),
        (["1", "2", "a", "A", "b", "_"], 2),
        (Config.SYMBOLS, 2),
    ],
)
def test_generate_short_url(symbols, length, app):
    """
    проверка на генерацию уникальных ссылок в рамках одной длины
    проверка на правильную работу функции при переполнении
    """
    with app.app_context():
        for i in range(0, len(symbols) ** length + 1):
            database.session.add(
                Url(
                    original_url="https://google.com",
                    short_url=generate_short_url(symbols=symbols, length=length),
                )
            )
        assert (
            len(
                database.session.query(Url)
                .order_by(func.length(Url.short_url).desc())
                .first()
                .short_url
            )
            > length
        )
