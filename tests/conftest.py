import pytest

from app import create_app, database
from app.model import Url
from app.settings import TestConfig


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)

    yield app
    with app.app_context():
        database.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def create_data(request, app):
    with app.app_context():
        database.session.add(Url(**request.param))
        database.session.commit()
    yield request.param
    with app.app_context():
        Url.query.filter_by(short_url=request.param["short_url"]).delete()
        database.session.commit()
