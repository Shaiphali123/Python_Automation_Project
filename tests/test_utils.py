import sys
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from app.constants import SECRET_KEY, ALGORITHM
from app.utils import create_access_token

access_token = "2w3e4r5t6y7u.3e4r5t6y7u.4er5t6y7";

# Test Case 1: Test when expires_delta is provided
def test_create_access_token_with_expires_delta():
    # Mock the jwt.encode function
    with patch("jwt.encode") as mock_encode:
        mock_encode.return_value = access_token

        # Data to encode in the token
        data = {"sub": "user123"}
        expires_delta = timedelta(minutes=30)

        # Call the function
        token = create_access_token(data, expires_delta)

        # Check that jwt.encode was called with the correct arguments
        mock_encode.assert_called_once_with(
            {**data, "exp": datetime.utcnow() + expires_delta},
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        # Verify the returned value is as expected
        assert token == access_token




# Test Case 2: Test when expires_delta is not provided (should default to 15 minutes)
def test_create_access_token_without_expires_delta():
    # Mock the jwt.encode function to avoid real JWT token creation
    with patch("jwt.encode") as mock_encode:
        # Mock the return value of jwt.encode
        mock_encode.return_value = "mocked_jwt_token"

        # Data to encode in the token
        data = {"sub": "user123"}

        # Call the function without passing expires_delta (it should default to 15 minutes)
        token = create_access_token(data)

        # Check that jwt.encode was called with the correct arguments
        mock_encode.assert_called_once_with(
            {**data, "exp": timedelta(minutes=15) + datetime.utcnow()},
            "4e9350f4-76c9-4c2d-9eaf-dd68ed7ac31a",  # Secret key from constants
            algorithm="HS256"  # Algorithm from constants
        )

        # Verify the returned value matches the mocked JWT token
        assert token == "mocked_jwt_token"

