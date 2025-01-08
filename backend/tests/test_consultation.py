import requests
import pytest
import random
import string



ENDPOINT = 'http://127.0.0.1:8000/api/'

# Global variable
consultation_id = None
medecin_user_name = None
medecin_password = None
patient_user_name = None
nss = None

"""
create account
create patient
create dpi
"""

def test_create_account_medecin():
    global medecin_user_name , medecin_password
    medecin_user_name , medecin_password = generate_random_username_and_password()
    payload = {
        "username": medecin_user_name,
        "password": medecin_password,
        "role": "medecin"
    }
    response = requests.post(ENDPOINT + 'signup/', json=payload)
    assert response.status_code == 201, f"Account creation failed: {response.text}"


@pytest.fixture(scope="session")
def login_token():
    """
    A pytest fixture to handle login and return the access token for reuse.
    """
    payload = {
        "username": medecin_user_name,
        "password": medecin_password
    }
    response = requests.post(ENDPOINT + 'login/', json=payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()['access']

def test_create_account_patient():
    global patient_user_name
    patient_user_name , password = generate_random_username_and_password()
    payload = {
        "username": patient_user_name,
        "password": password,
        "role": "patient"
    }
    response = requests.post(ENDPOINT + 'signup/', json=payload)
    assert response.status_code == 201, f"Account creation failed: {response.text}"

def test_create_dpi(login_token):
    headers = {"Authorization": f"Bearer {login_token}"}
    global nss
    nss = random.randint(1, 9999999)
    payload = {
        "patient":patient_user_name ,
        "medecin_traitant":medecin_user_name ,
        "nss":nss ,
        "date_naissance":"2021-06-01" ,
        "adresse":"rue de la paix" ,
        "telephone":"0612345678" ,
        "mutuelle":"mutuelle" ,
        "personne_a_contacter":"personne"
    }
    response = requests.post(ENDPOINT + 'dpi/create/', json=payload, headers=headers)
    assert response.status_code == 201, f"DPI creation failed: {response.text}"

def test_consultation_list(login_token):
    headers = {"Authorization": f"Bearer {login_token}"}
    response = requests.get(ENDPOINT + f"dpi/{nss}/consultation/all/", headers=headers)
    assert response.status_code == 200


def test_consultation_create(login_token):
    global consultation_id
    payload = {
        "motif": "maladie"
    }
    headers = {"Authorization": f"Bearer {login_token}"}
    response = requests.post(ENDPOINT + f"dpi/{nss}/consultation/all/", json=payload, headers=headers)
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

def generate_random_username_and_password():
    length = 10
    username_chars = string.ascii_letters + string.digits
    password_chars = string.ascii_letters + string.digits + string.punctuation
    username = ''.join(random.choices(username_chars, k=length))
    password = ''.join(random.choices(password_chars, k=length))
    return username, password



def create_account(payload):
    response = requests.post(ENDPOINT + 'signup/', json=payload)
    assert response.status_code == 201, f"Account creation failed: {response.text}"

