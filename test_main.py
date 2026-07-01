from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_job():
    response = client.post("/jobs/", json={
        "title": "Backend Developer",
        "company": "Acme Inc",
        "description": "Build APIs",
        "location": "Remote"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Backend Developer"
    assert "id" in data

def test_get_nonexistent_applicant():
    response = client.get("/applicants/99999")
    assert response.status_code == 404