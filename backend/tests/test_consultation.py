import requests

ENDPOINT = 'http://127.0.0.1:8000/api/'

def test_consultation_list():
    response = requests.get(ENDPOINT + 'dpi/2333/consultation/all/') 
    assert response.status_code == 200

def test_consultation_create():
    payload = {
        "motif" : "maladie"
    }
    response = requests.post(ENDPOINT + 'dpi/2333/consultation/all/', json=payload)
    assert response.status_code == 201

def test_consultation_detail():
    response = requests.get(ENDPOINT + 'dpi/consultation/3/') 
    assert response.status_code == 200

def test_consultation_update():
    payload = {
        "motif" : "maladies",
        "resume" : "test"
    }
    response = requests.put(ENDPOINT + 'dpi/consultation/3/', json=payload)
    assert response.status_code == 200
    assert response.json()['resume'] == payload['resume']

def test_consultation_delete():
    response = requests.delete(ENDPOINT + 'dpi/consultation/3/')
    assert response.status_code == 204


