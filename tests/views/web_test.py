import pytest

from app.model import Url


def test_get_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert (
        '<input type="text" name="original_url" placeholder="Введите URL" class="" /><br>'
        in response.text
    )


def test_get_index_error(client):
    response = client.get("/aboba")
    assert response.status_code == 200
    assert "this url does not exist" in response.text


@pytest.mark.parametrize(
    "create_data",
    [{"original_url": "https://google.com", "short_url": "aboba"}],
    indirect=True,
)
def test_redirect(client, create_data, app):
    with app.app_context():
        assert (
            Url.query.filter_by(short_url=create_data["short_url"]).scalar().count == 0
        )
    response = client.get(f"/{create_data['short_url']}")
    assert response.status_code == 302
    assert create_data["original_url"] in response.text
    with app.app_context():
        assert (
            Url.query.filter_by(short_url=create_data["short_url"]).scalar().count == 1
        )
