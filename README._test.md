Bookstore API - Unit and Integration Testing
Project Overview
This project is a simple Bookstore API built with FastAPI. It allows users to manage books and perform user authentication, including sign-up and login functionalities. The API uses JWT tokens for securing endpoints related to book management.

Testing Strategy
1. Unit Testing
Unit tests are written to ensure individual components of the API work as expected. The main focus is to test functions, methods, and services in isolation from external dependencies like databases or APIs.

Authentication Tests: Testing user authentication such as login and signup.
Book Management Tests: Testing CRUD operations for book management.
2. Integration Testing
Integration tests ensure that different parts of the application work together as expected. These tests simulate real-world API usage and validate interactions between multiple components, like database, routes, and services.

Book Management API Endpoints: Testing the interaction between routes and the database for adding, updating, deleting, and retrieving books.
JWT Token Authentication: Testing access control for secured endpoints, ensuring only authenticated users can interact with book management.
Running the Tests
1. Install Dependencies
First, make sure to install all required dependencies by running the following command:


pip install -r requirements.txt
This will install the necessary packages, including pytest, pytest-cov, pytest-html, and FastAPI.

2. Run Unit Tests
Unit tests are designed to test individual components. To run the unit tests and check for code coverage, use the following command:


pytest --cov=your_module_name --cov-report=html --html=report.html
This command will:

Run all unit tests.
Generate a code coverage report in htmlcov/ directory.
Generate an HTML report of the test results in report.html.
3. Run Unit and Integration Tests
To run both unit and integration tests, ensuring that interactions between components are properly tested, use:


pytest tests/ --cov=your_module_name --cov-report=html --html=report.html
This will:

Run all tests in the tests/ directory (including unit and integration tests).
Generate both the code coverage report and HTML test report.

4. View Reports
The code coverage report can be found in the htmlcov/index.html file. Open it in your browser to view which parts of your code are covered by the tests.
The test result report can be found in the report.html file.

5. Fixtures for Testing

JWT Token Fixture: A fixture is used to generate a JWT token for authenticating user-related endpoints.
Test Client: The tests use a FastAPI test client (TestClient) to send HTTP requests to the API and receive responses for verification.
Example of a Fixture to Get an Access Token:

@pytest.fixture(scope="session")
def access_token(client):
    user_credentials = {"email": "test@example.com", "password": "password123"}
    response = client.post("/login", json=user_credentials)
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None
    return token


Example of Unit and Integration Tests
Unit Test Example:

def test_user_signup(client):
    user_data = {"email": "newuser@example.com", "password": "password123"}
    response = client.post("/signup", json=user_data)
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}


Integration Test Example:

def test_book_management(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    new_book = {
        "name": "Test Book",
        "author": "Test Author",
        "published_year": 2024,
        "book_summary": "Test Summary"
    }
    response = client.post("/books/", json=new_book, headers=headers)
    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
    assert response_data["name"] == new_book["name"]
    assert response_data["author"] == new_book["author"]


6. Challenges Faced
JWT Token Management: Ensuring that authentication tokens are generated and validated correctly was a critical part of securing endpoints. We created fixtures to handle token generation and passing the token to test protected routes.

Database Cleanup: During testing, ensuring that the database is cleaned between tests to avoid data leakage was a challenge. Using database transactions for each test and rolling back at the end of the test was a solution we used.

Conclusion
This Bookstore API includes comprehensive unit and integration testing to ensure the functionality and security of the application. By running the tests locally, you can verify both individual components and their integrations with the database, ensuring a reliable and secure API.

GitHub Repository
https://github.com/Shaiphali123/Python_Automation_Project/tree/main


