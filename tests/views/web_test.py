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


def test_post_index(client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "original_url": "http://google.com",
        "short_url": "http://127.0.0.1/aboba",
    }
    mock = mocker.patch("app.views.web.requests.post", return_value=mock_response)
    response = client.post("/")
    assert response.status_code == 200
    assert "http://google.com" in response.text
    assert "http://127.0.0.1/aboba" in response.text


def test_post_index_error(client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 422
    mock_response.text = """<h1>Unprocessable Content</h1><p>try again, this short url already exist</p>"""
    mock = mocker.patch("app.views.web.requests.post", return_value=mock_response)
    response = client.post("/")
    assert response.status_code == 422
    assert "Unprocessable Content" in response.text
