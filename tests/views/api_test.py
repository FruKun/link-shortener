import pytest
from flask import json, render_template


def test_get_urls_not_valid_method(client):
    responce = client.get("/api/urls")
    assert responce.status_code == 405


def test_delete_urls_not_valid_method(client):
    responce = client.delete("/api/urls")
    assert responce.status_code == 405


def test_put_urls_not_valid_method(client):
    responce = client.put("/api/urls")
    assert responce.status_code == 405


def test_patch_urls_not_valid_method(client):
    responce = client.patch("/api/urls")
    assert responce.status_code == 405


@pytest.mark.parametrize(
    "data",
    [
        "{}",
        "",
        {"aboba": ""},
        {"aboba": "aboba"},
        {"original_url": ""},
        {"original_url": "aboba"},
        {"original_url": "google.com"},
        {"original_url": "http://"},
        {"original_url": "http//google.com"},
        {"original_url": "http/google.com"},
        {"original_url": "http:/google.com"},
        {"original_url": "https://"},
        {"original_url": "https//google.com"},
        {"original_url": "https/google.com"},
        {"original_url": "https:/google.com"},
        {"original_url": "http:/googlecom"},
        {"original_url": "https://googlecom"},
        {"original_url": "aboba://google.com"},
        {"original_url": "123://google.com"},
    ],
)
def test_post_urls_not_valid_original_url(client, data):
    responce = client.post("/api/urls", data=json.dumps(data))
    assert responce.status_code == 422
    assert responce.json == "422 Unprocessable Entity: original url Validation error"


@pytest.mark.parametrize(
    "data",
    [
        {"original_url": "https://google.com"},
        {"original_url": "https://google.com", "short_url": ""},
        {"original_url": "https://google.com", "short": "a"},
    ],
)
def test_post_urls_valid_original_url(client, data):
    responce = client.post("/api/urls", data=json.dumps(data))
    assert responce.status_code == 200
    assert responce.json["original_url"] == "https://google.com"
    assert len(responce.json["short_url"].split("/")[1]) == 4


@pytest.mark.parametrize(
    "short_url",
    [
        "aboba",
        "epope",
        "a" * 300,
        1234,
        "1234",
        ".~-_",
    ],
)
def test_post_urls_expected_short_url(client, short_url):
    data = {"original_url": "https://google.com", "short_url": short_url}
    responce = client.post("/api/urls", data=json.dumps(data))
    assert responce.status_code == 200
    assert responce.json["original_url"] == "https://google.com"
    assert responce.json["short_url"].split("/")[1] == str(short_url)


@pytest.mark.parametrize("short_url", ["`", ",", "'", '"', "/", "?", "aboba\\"])
def test_post_urls_unexpected_short_url(client, short_url):
    data = {"original_url": "https://google.com", "short_url": short_url}
    responce = client.post("/api/urls", data=json.dumps(data))
    assert responce.status_code == 422
    assert responce.json == "422 Unprocessable Entity: short url Validation error"


@pytest.mark.parametrize(
    "create_data",
    [{"original_url": "https://google.com", "short_url": "uniq_aboba"}],
    indirect=True,
)
def test_post_urls_unique_short_url(client, create_data):
    responce = client.post("/api/urls", data=json.dumps(create_data))
    assert responce.status_code == 422
    assert (
        responce.json
        == "422 Unprocessable Entity: try again, this short url already exist"
    )


def test_get_doc(client, app):
    responce = client.get("/api/doc")
    assert responce.status_code == 200
    with app.app_context():
        assert responce.text == render_template("doc.html")


def test_post_doc_not_valid_method(client):
    responce = client.post("/api/doc")
    assert responce.status_code == 405


def test_delete_doc_not_valid_method(client):
    responce = client.delete("/api/doc")
    assert responce.status_code == 405


def test_put_doc_not_valid_method(client):
    responce = client.put("/api/doc")
    assert responce.status_code == 405


def test_patch_doc_not_valid_method(client):
    responce = client.patch("/api/doc")
    assert responce.status_code == 405
