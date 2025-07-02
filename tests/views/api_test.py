import json

import pytest


def test_get_urls_not_valid_method(client):
    response = client.get("/api/urls")
    assert response.status_code == 302


def test_delete_urls_not_valid_method(client):
    response = client.delete("/api/urls")
    assert response.status_code == 405


def test_put_urls_not_valid_method(client):
    response = client.put("/api/urls")
    assert response.status_code == 405


def test_patch_urls_not_valid_method(client):
    response = client.patch("/api/urls")
    assert response.status_code == 405


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
    response = client.post("/api/urls", data=json.dumps(data))
    assert response.status_code == 422
    assert "original url Validation error" in response.text


@pytest.mark.parametrize(
    "data",
    [
        {"original_url": "https://google.com"},
        {"original_url": "https://google.com", "short_url": ""},
        {"original_url": "https://google.com", "short": "a"},
    ],
)
def test_post_urls_valid_original_url(client, data):
    response = client.post("/api/urls", data=json.dumps(data))
    assert response.status_code == 200
    assert response.json["original_url"] == "https://google.com"
    assert len(response.json["short_url"].split("/")[3]) == 4


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
    response = client.post("/api/urls", data=json.dumps(data))
    assert response.status_code == 200
    assert response.json["original_url"] == "https://google.com"
    assert response.json["short_url"].split("/")[3] == str(short_url)


@pytest.mark.parametrize("short_url", ["`", ",", "'", '"', "/", "?", "aboba\\"])
def test_post_urls_unexpected_short_url(client, short_url):
    data = {"original_url": "https://google.com", "short_url": short_url}
    response = client.post("/api/urls", data=json.dumps(data))
    assert response.status_code == 422
    assert "short url Validation error" in response.text


@pytest.mark.parametrize(
    "create_data",
    [{"original_url": "https://google.com", "short_url": "uniq_aboba"}],
    indirect=True,
)
def test_post_urls_unique_short_url(client, create_data):
    response = client.post("/api/urls", data=json.dumps(create_data))
    assert response.status_code == 422
    assert "try again, this short url already exist" in response.text


def test_get_doc(client):
    response = client.get("/api/")
    assert response.status_code == 200
    assert "json request example:" in response.text


def test_post_doc_not_valid_method(client):
    response = client.post("/api/doc")
    assert response.status_code == 405


def test_delete_doc_not_valid_method(client):
    response = client.delete("/api/doc")
    assert response.status_code == 405


def test_put_doc_not_valid_method(client):
    response = client.put("/api/doc")
    assert response.status_code == 405


def test_patch_doc_not_valid_method(client):
    response = client.patch("/api/doc")
    assert response.status_code == 405
