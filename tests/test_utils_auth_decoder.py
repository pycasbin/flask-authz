import jwt
import pytest
from flask_authz.utils import authorization_decoder, UnSupportedAuthType


@pytest.mark.parametrize("auth_str, result", [("Basic Ym9iOnBhc3N3b3Jk", "Bob")])
def test_auth_docode(app_fixture, auth_str, result):
    assert authorization_decoder(app_fixture.config, auth_str) == "bob"


@pytest.mark.parametrize(
    "auth_str, result",
    [
        (
            "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6IkJvYiJ9"
            ".YZqkPHdrxkkFNg7GNL8g-hRpiD9LPyospO47Mh3iEDk",
            "Bob",
        )
    ],
)
def test_auth_docode(app_fixture, auth_str, result):
    assert authorization_decoder(app_fixture.config, auth_str) == "Bob"


@pytest.mark.parametrize("auth_str", [("Unsupported Ym9iOnBhc3N3b3Jk")])
def test_auth_docode_exceptions(app_fixture, auth_str):
    with pytest.raises(UnSupportedAuthType):
        authorization_decoder(app_fixture.config, auth_str)


@pytest.mark.parametrize(
    "auth_str",
    [
        (
            "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTUxMDg0OTIuNTY5MjksImlkZW50aXR5IjoiQm9iIn0."
            "CAeMpG-gKbucHU7-KMiqM7H_gTkHSRvXSjNtlvh5DlE"
        )
    ],
)
def test_auth_docode_exceptions(app_fixture, auth_str):
    with pytest.raises(jwt.ExpiredSignatureError):
        authorization_decoder(app_fixture.config, auth_str)
