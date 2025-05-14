from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_security_headers():
    response = client.get("/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"

def test_logging_middleware(caplog):
    with caplog.at_level(logging.INFO):
        client.get("/health")
        assert "Request: GET http://testserver/health" in caplog.text
        assert "Response status: 200" in caplog.text
