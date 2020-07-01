import os
import flask
import pytest


@pytest.fixture
def app_fixture():
    app = flask.Flask("test")
    app.testing = True
    app.config["CASBIN_MODEL"] = (
        os.path.split(os.path.realpath(__file__))[0] + "/casbin_files/rbac_model.conf"
    )
    # Set headers where owner for enforcement policy should be located
    app.config["CASBIN_OWNER_HEADERS"] = {"Authorization", "X-User", "X-Idp-Groups"}

    yield app
