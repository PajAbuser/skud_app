import json
from uuid import UUID
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

def test_add_pass(api_client):
    data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}}
    response = api_client.post('/add_pass/', data, format='json')
    assert response.status_code == 201

def test_repr_pass(api_client):
    response = api_client.get('/passes/1/')
    assert response.status_code == 200

def test_repr_passes(api_client):
    response = api_client.get('/passes/')
    assert response.status_code == 200

def test_add_door(api_client):
    data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}}
    response = api_client.post('/add_door/', data, format='json')
    assert response.status_code == 201

def test_repr_door(api_client):
    response = api_client.get('/doors/1/')
    assert response.status_code == 200

def test_repr_doors(api_client):
    response = api_client.get('/doors/')
    assert response.status_code == 200

def test_add_door_pass(api_client):
    data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}, 
            'Pass': {'UUID': '23456789-2345-2345-2345-234567890123'}}
    response = api_client.post('/doors/1/passes/', data, format='json')
    assert response.status_code == 201

def test_remove_passes(api_client):
    data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}, 
            'Passes': [{'UUID': '23456789-2345-2345-2345-234567890123'}]}
    response = api_client.delete('/doors/1/passes/', data, format='json')
    assert response.status_code == 204

def test_remove_pass(api_client):
    door_id = 1
    pass_id = 1
    response = api_client.delete(f'/doors/{door_id}/passes/{pass_id}/')
    assert response.status_code == 204

def test_check1(api_client):
    data = {'Door': {'UUID': '12345678-1234-1234-1234-123456789012'}, 
            'Pass': {'UUID': '23456789-2345-2345-2345-234567890123'}}
    response = api_client.post('/check/', data, format='json')
    assert response.status_code == 200

def test_check2(api_client):
    door_id = 1
    pass_id = 1
    response = api_client.get(f'/check/{door_id}/{pass_id}/')
    assert response.status_code == 200

def test_get_operation(api_client):
    id = UUID('12345678-1234-1234-1234-123456789012')
    response = api_client.get(f'/getOperation/{id}/')
    assert response.status_code == 200