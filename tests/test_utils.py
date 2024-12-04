import sys
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from app.constants import SECRET_KEY, ALGORITHM
from app.utils import create_access_token

access_token = "2w3e4r5t6y7u.3e4r5t6y7u.4er5t6y7";


def test_create_access_token_with_expires_delta():

    with patch("jwt.encode") as mock_encode:
        mock_encode.return_value = access_token


        data = {"sub": "user123"}
        expires_delta = timedelta(minutes=30)


        token = create_access_token(data, expires_delta)


        mock_encode.assert_called_once_with(
            {**data, "exp": datetime.utcnow() + expires_delta},
            SECRET_KEY,
            algorithm=ALGORITHM
        )


        assert token == access_token




#
def test_create_access_token_without_expires_delta():

    with patch("jwt.encode") as mock_encode:

        mock_encode.return_value = "mocked_jwt_token"


        data = {"sub": "user123"}


        token = create_access_token(data)


        mock_encode.assert_called_once_with(
            {**data, "exp": timedelta(minutes=15) + datetime.utcnow()},
            "4e9350f4-76c9-4c2d-9eaf-dd68ed7ac31a",
            algorithm="HS256"
        )


        assert token == "mocked_jwt_token"

