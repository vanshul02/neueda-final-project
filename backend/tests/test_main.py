import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_signup():
    response = client.post("/auth/signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_deposit():
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/transactions/deposit", json={"amount": 100.0}, headers=headers)
    assert response.status_code == 200
    assert response.json()["amount"] == 100.0

def test_withdraw():
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/transactions/withdraw", json={"amount": 50.0}, headers=headers)
    assert response.status_code == 200
    assert response.json()["amount"] == -50.0

def test_transaction_history():
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
