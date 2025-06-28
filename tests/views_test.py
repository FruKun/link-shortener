import pytest


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"aboba" in response.data
