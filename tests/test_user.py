from unittest.mock import MagicMock

import pytest
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database import UserCredentials

from app.main import create_user_signup, login_for_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock database session
@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


# Test user signup
@pytest.mark.anyio
async def test_create_user_signup(mock_db):
    # Mock existing user
    mock_db.query.return_value.filter.return_value.first.return_value = None

    user_credentials = UserCredentials(email="test@example.com", password="password123")
    response = await create_user_signup(user_credentials, db=mock_db)

    assert response["message"] == "User created successfully"


@pytest.mark.anyio
async def test_create_user_signup_existing_user(mock_db):
    # Mock existing user
    mock_db.query.return_value.filter.return_value.first.return_value = UserCredentials(
        email="test@example.com", password="hashed_password"
    )

    user_credentials = UserCredentials(email="test@example.com", password="password123")

    with pytest.raises(HTTPException) as excinfo:
        await create_user_signup(user_credentials, db=mock_db)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Email already registered"


# Test login
@pytest.mark.anyio
async def test_login_for_access_token(mock_db):
    hashed_password = pwd_context.hash("password123")
    mock_db.query.return_value.filter.return_value.first.return_value = UserCredentials(
        email="test@example.com", password=hashed_password
    )

    user_credentials = UserCredentials(email="test@example.com", password="password123")
    response = await login_for_access_token(user_credentials, db=mock_db)

    assert "access_token" in response
    assert response["token_type"] == "bearer"

