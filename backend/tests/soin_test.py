import pytest
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Soin, DPI, Infirmier, Patient, Medecin
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_soin():
    # Create a user, patient, and medecin
    medecin_user = User.objects.create_user(username="medecin1", password="password123")
    medecin = Medecin.objects.create(user=medecin_user, specialite="Cardiologie")

    patient_user = User.objects.create_user(username="patient1", password="password123")
    patient = Patient.objects.create(user=patient_user, adresse="123 Rue Example", telephone="123456789")

    # Create a DPI for the patient
    dpi = DPI.objects.create(
        patient=patient,
        medecin_traitant=medecin,
        nss="123456789012345",
        date_naissance="1990-01-01",
        adresse="123 Rue Example",
        telephone="123456789"
    )

    # Create an Infirmier
    infirmier_user = User.objects.create_user(username="infirmier1", password="password123")
    infirmier = Infirmier.objects.create(user=infirmier_user)

    # Prepare data for the 'Soin' creation
    soin_data = {
        "dpi": dpi.id,
        "infirmier": infirmier.id,
        "description": "Test Soin",
        "observations": "No issues"
    }

    # Send POST request to create the Soin
    client = APIClient()
    response = client.post('/dpi/soin/create/', soin_data, format='json')

    # Check response status and ensure the Soin is created
    assert response.status_code == status.HTTP_201_CREATED
    assert Soin.objects.count() == 1  # Ensure 1 Soin is created
    assert response.data['description'] == soin_data['description']  # Validate description


@pytest.mark.django_db
def test_get_soins():
    # Create a user, patient, and medecin
    medecin_user = User.objects.create_user(username="medecin1", password="password123")
    medecin = Medecin.objects.create(user=medecin_user, specialite="Cardiologie")

    patient_user = User.objects.create_user(username="patient1", password="password123")
    patient = Patient.objects.create(user=patient_user, adresse="123 Rue Example", telephone="123456789")

    # Create a DPI for the patient
    dpi = DPI.objects.create(
        patient=patient,
        medecin_traitant=medecin,
        nss="123456789012345",
        date_naissance="1990-01-01",
        adresse="123 Rue Example",
        telephone="123456789"
    )

    # Create an Infirmier
    infirmier_user = User.objects.create_user(username="infirmier1", password="password123")
    infirmier = Infirmier.objects.create(user=infirmier_user)

    # Create Soin
    Soin.objects.create(
        dpi=dpi,
        infirmier=infirmier,
        description="Test Soin 1",
        observations="No issues"
    )

    # Get the list of 'soins'
    client = APIClient()
    response = client.get('/dpi/soins/')  # Update the URL to /dpi/soins/

    # Check response status and ensure correct data is returned
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_soin():
    # Create a user, patient, and medecin
    medecin_user = User.objects.create_user(username="medecin1", password="password123")
    medecin = Medecin.objects.create(user=medecin_user, specialite="Cardiologie")

    patient_user = User.objects.create_user(username="patient1", password="password123")
    patient = Patient.objects.create(user=patient_user, adresse="123 Rue Example", telephone="123456789")

    # Create a DPI for the patient
    dpi = DPI.objects.create(
        patient=patient,
        medecin_traitant=medecin,
        nss="123456789012345",
        date_naissance="1990-01-01",
        adresse="123 Rue Example",
        telephone="123456789"
    )

    # Create an Infirmier
    infirmier_user = User.objects.create_user(username="infirmier1", password="password123")
    infirmier = Infirmier.objects.create(user=infirmier_user)

    # Create a Soin
    soin = Soin.objects.create(
        dpi=dpi,
        infirmier=infirmier,
        description="Test Soin",
        observations="No issues"
    )

    # Prepare updated data for the Soin
    updated_data = {
        "description": "Updated Soin Description",
        "observations": "Updated observations"
    }

    # Send PATCH request to update the Soin
    client = APIClient()
    response = client.patch(f'/dpi/soin/{soin.id}/', updated_data, format='json')

    # Check response status and ensure the Soin is updated
    assert response.status_code == status.HTTP_200_OK
    assert response.data['description'] == updated_data['description']  # Validate updated description


@pytest.mark.django_db
def test_delete_soin():
    # Create a user, patient, and medecin
    medecin_user = User.objects.create_user(username="medecin1", password="password123")
    medecin = Medecin.objects.create(user=medecin_user, specialite="Cardiologie")

    patient_user = User.objects.create_user(username="patient1", password="password123")
    patient = Patient.objects.create(user=patient_user, adresse="123 Rue Example", telephone="123456789")

    # Create a DPI for the patient
    dpi = DPI.objects.create(
        patient=patient,
        medecin_traitant=medecin,
        nss="123456789012345",
        date_naissance="1990-01-01",
        adresse="123 Rue Example",
        telephone="123456789"
    )

    # Create an Infirmier
    infirmier_user = User.objects.create_user(username="infirmier1", password="password123")
    infirmier = Infirmier.objects.create(user=infirmier_user)

    # Create a Soin
    soin = Soin.objects.create(
        dpi=dpi,
        infirmier=infirmier,
        description="Test Soin",
        observations="No issues"
    )

    # Send DELETE request to remove the Soin
    client = APIClient()
    response = client.delete(f'/dpi/soins/delete/{soin.id}/')

    # Ensure the response status code is 204 and the Soin is deleted
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Soin.objects.count() == 0  # Ensure no 'Soin' remains


