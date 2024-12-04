import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    # Synchronous TestClient
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def access_token(client):

    user_credentials = {"email": "shaiphalinwd76165@gmail.com", "password": "12345678"}


    response = client.post("/login", json=user_credentials)
    print(response.json())
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None
    return token

def test_book_management(client,access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    new_book = {
        "name": "Test Book",
        "author": "Test Author",
        "published_year": 2024,
        "book_summary": "Test Summary"
    }
    response = client.post("/books/", json=new_book, headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    book_id = response_data["id"]
    print(f"Created Book ID: {book_id}")
    assert response_data["name"] == new_book["name"]
    assert response_data["author"] == new_book["author"]
def test_get_all_books(client, access_token):

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/books/", headers=headers)
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)

def test_get_book_by_id(client, access_token):

    headers = {"Authorization": f"Bearer {access_token}"}
    new_book = {
        "name": "Test Book by ID",
        "author": "Test Author",
        "published_year": 2023,
        "book_summary": "A test summary for the book."
    }

    create_response = client.post("/books/", json=new_book, headers=headers)
    assert create_response.status_code == 200
    book_id = create_response.json()["id"]


    response = client.get(f"/books/{book_id}", headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == book_id
    assert response_data["name"] == new_book["name"]

def test_update_book(client, access_token):

    headers = {"Authorization": f"Bearer {access_token}"}
    new_book = {
        "name": "Original Book",
        "author": "Original Author",
        "published_year": 2022,
        "book_summary": "Original summary."
    }

    create_response = client.post("/books/", json=new_book, headers=headers)
    assert create_response.status_code == 200
    book_id = create_response.json()["id"]


    updated_book = {
        "name": "Updated Book",
        "author": "Updated Author",
        "published_year": 2023,
        "book_summary": "Updated summary."
    }
    response = client.put(f"/books/{book_id}", json=updated_book, headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == updated_book["name"]
    assert response_data["author"] == updated_book["author"]

def test_delete_book(client, access_token):
    """Test deleting a book."""
    headers = {"Authorization": f"Bearer {access_token}"}
    new_book = {
        "name": "Book to Delete",
        "author": "Author to Delete",
        "published_year": 2021,
        "book_summary": "Summary for deletion."
    }

    create_response = client.post("/books/", json=new_book, headers=headers)
    assert create_response.status_code == 200
    book_id = create_response.json()["id"]


    response = client.delete(f"/books/{book_id}", headers=headers)
    assert response.status_code == 200


    get_response = client.get(f"/books/{book_id}", headers=headers)
    assert get_response.status_code == 404









