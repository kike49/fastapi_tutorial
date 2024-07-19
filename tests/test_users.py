from jose import jwt
from app import schemas
from app.config import settings
import pytest
 
# Test the login of the user created in the fixtures (conftest.py)
def test_login_user(client, create_test_user):
    response = client.post("/login/", data={"username": create_test_user["email"], "password": create_test_user["password"]})
    login_response = schemas.Token(**response.json())
    payload = jwt .decode(login_response.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITIHM])
    id = payload.get("user_id")
    assert int(id) == create_test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

# Test the client logged in for a request in a protected route
def test_authorized_login_request(create_authorized_test_client):
    response = create_authorized_test_client.get("/posts/")
    assert response.status_code == 200

# Test the log in with several wrong email, passwords or empty fields
@pytest.mark.parametrize("email, password, status_code", [("wrong_email@example.com", "correctPassword", 403), ("correct_email@example.com", "wrongPassword", 403), ("wrong_email@example.com", "wrongPassword", 403), (None, "correctPassword", 422), ("correct_email@example.com", None, 422)]) # 422 -> schema validation failed because of empty fields
def test_incorrect_login(client, email, password, status_code):
    wrong_user = {"username": email, "password": password}
    response = client.post("/login", data=wrong_user)
    assert response.status_code == status_code