from fastapi.testclient import TestClient
from main import app

# Create a fake client to send requests to our app
client = TestClient(app)

def test_add_user():
    # Simulate a POST request to add a user
    response = client.post(
        "/users/99",
        json={"name": "Test User", "email": "test@example.com"}
    )
    
    # Check that the API returns a 201 Created status code
    assert response.status_code == 201
    # Check that the response body matches what we expect
    assert response.json()["message"] == "User added"