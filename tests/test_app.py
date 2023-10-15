import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/ping')
    assert response.status_code == 200

def test_get_keywords_returns_list(client):
    response = client.get('/keyword')
    assert type(response.json['keywords']) == list