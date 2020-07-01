import pytest
from flask_authz.utils import authorization_decoder, UnSupportedAuthType


@pytest.mark.parametrize("auth_str, result", [("Basic Ym9iOnBhc3N3b3Jk", "Bob")])
def test_auth_docode(auth_str, result):
    assert authorization_decoder(auth_str) == "bob"


@pytest.mark.parametrize(
    "auth_str", [("Bearer Ym9iOnBhc3N3b3Jk"), ("Unsupported Ym9iOnBhc3N3b3Jk")]
)
def test_auth_docode_exceptions(auth_str):
    with pytest.raises(UnSupportedAuthType):
        authorization_decoder(auth_str)
