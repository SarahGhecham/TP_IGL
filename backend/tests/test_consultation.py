import requests
import pytest

ENDPOINT = 'http://127.0.0.1:8000/api/'

# Global variable
consultation_id = None

consultation_id = 0
@pytest.fixture(scope="session")
def login_token():
    """
    A pytest fixture to handle login and return the access token for reuse.
    """
    payload = {
        "username": "cse",
        "password": "cse"
    }
    response = requests.post(ENDPOINT + 'login/', json=payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()['access']


def test_consultation_list(login_token):
    headers = {"Authorization": f"Bearer {login_token}"}
    response = requests.get(ENDPOINT + 'dpi/2333/consultation/all/', headers=headers)
    assert response.status_code == 200


def test_consultation_create(login_token):
    global consultation_id
    payload = {
        "motif": "maladie"
    }
    headers = {"Authorization": f"Bearer {login_token}"}
    response = requests.post(ENDPOINT + 'dpi/2333/consultation/all/', json=payload, headers=headers)
    assert response.status_code == 201
    consultation_id = response.json()['id']


def test_consultation_detail(login_token):
    headers = {"Authorization": f"Bearer {login_token}"}
    response = requests.get(ENDPOINT + f"dpi/consultation/{consultation_id}/", headers=headers)
    assert response.status_code == 200


def test_consultation_update(login_token):
    payload = {
        "motif": "maladies",
        "resume": "test"
    }
    headers = {"Authorization": f"Bearer {login_token}"}
    response = requests.put(ENDPOINT + f"dpi/consultation/{consultation_id}/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()['resume'] == payload['resume']


def test_consultation_delete(login_token):
    headers = {"Authorization": f"Bearer {login_token}"}
    response = requests.delete(ENDPOINT + f"dpi/consultation/{consultation_id}/", headers=headers)
    assert response.status_code == 204


