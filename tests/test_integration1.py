import pytest
from fastapi.testclient import TestClient
from app.main import app  # Replace with your actual FastAPI app

@pytest.fixture(scope="module")
def client():
    # Synchronous TestClient
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
def access_token(client):
    # Assuming you already have a test user registered
    user_credentials = {"email": "shaiphalinwd101@gmail.com", "password": "password12345@"}

    # Login to get access token
    response = client.post("/login", json=user_credentials)
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None
    return token


def test_health_check(client):
    response = client.get("/health")  # No await needed
    assert response.status_code == 200
    assert response.json() == {"status": "up"}

def test_user_authentication_signup_already_exist(client):
    response = client.post("/signup", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_user_authentication_signup_new_user(client):
    response = client.post("signup",json={"email": "shaiphalinwd76165@gmail.com","password":"12345678"})
    assert response.status_code == 200
    assert response.json() == {'message': 'User created successfully'}

def test_user_login_valid(client):
    response = client.post("/login", json={"email": "shaiphalinwd76165@gmail.com", "password": "12345678"})
    print(response.json())
#
    assert response.status_code == 200

    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_user_login_invalid(client):
    client.post("/signup",json = {"email":"shaiphalinwd1@gmail.com","password":"12345678"})
    response = client.post("/login", json={"email": "shaiphalinwd1lkjhjg@gmail.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    print(response.json())


"""def test_book_management(client):

    new_book = {
        "name": "Test Book",
        "author": "Test Author",
        "published_year": 2024,
        "book_summary": "Test Summary"
    }


    response = client.post("/books/", json=new_book)


    assert response.status_code == 201


    response_data = response.json()
    assert "id" in response_data
    assert response_data["name"] == new_book["name"]
    assert response_data["author"] == new_book["author"]
    assert response_data["published_year"] == new_book["published_year"]
    assert response_data["book_summary"] == new_book["book_summary"]


    book_id = response_data["id"]
"""