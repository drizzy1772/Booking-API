import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from booking.models import Resource
# Create your tests here.


@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_register(client):
    response = client.post("/api/register/", {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "testpass123"
    })
    assert response.status_code == 201
    assert response.data["username"] == "testuser"

@pytest.mark.django_db
def test_create_booking(client):
    user = User.objects.create_user(username="test", password="test12345")
    
    resource = Resource.objects.create(name='Room1', capacity=5)   
    
    client.force_authenticate(user=user)
    response = client.post("/api/booking/", {
        "resource_id": resource.id,
        "start_time": "2026-10-10T10:00:00Z",
        "end_time": "2026-10-10T11:00:00Z"
})
    assert response.status_code == 201


@pytest.mark.django_db
def test_double_booking(client):
    user = User.objects.create_user(username="test2", password="test12345")
    
    resource = Resource.objects.create(name='Room2', capacity=5)   
    
    client.force_authenticate(user=user)
    
    client.post("/api/booking/", {
        "resource_id": resource.id,
        "start_time": "2026-10-10T10:00:00Z",
        "end_time": "2026-10-10T11:00:00Z"
})
    
    response = client.post("/api/booking/", {
        "resource_id": resource.id,
        "start_time": "2026-10-10T10:00:00Z",
        "end_time": "2026-10-10T11:00:00Z"
    })
    
    assert response.status_code == 400