import pytest
from casbin.enforcer import Enforcer
from flask import request, jsonify
from casbin_sqlalchemy_adapter import Adapter
from casbin_sqlalchemy_adapter import Base
from casbin_sqlalchemy_adapter import CasbinRule
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_authz import CasbinEnforcer


@pytest.fixture
def enforcer(app_fixture):
    engine = create_engine("sqlite://")
    adapter = Adapter(engine)

    session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    s = session()
    s.query(CasbinRule).delete()
    s.add(CasbinRule(ptype="p", v0="alice", v1="/item", v2="GET"))
    s.add(CasbinRule(ptype="p", v0="bob", v1="/item", v2="GET"))
    s.add(CasbinRule(ptype="p", v0="data2_admin", v1="/item", v2="POST"))
    s.add(CasbinRule(ptype="p", v0="data2_admin", v1="/item", v2="DELETE"))
    s.add(CasbinRule(ptype="p", v0="data2_admin", v1="/item", v2="GET"))
    s.add(CasbinRule(ptype="g", v0="alice", v1="data2_admin"))
    s.add(CasbinRule(ptype="g", v0="users", v1="data2_admin"))
    s.add(CasbinRule(ptype="g", v0="group with space", v1="data2_admin"))
    s.commit()
    s.close()

    yield CasbinEnforcer(app_fixture, adapter)


@pytest.fixture
def watcher():
    class SomeWatcher:
        def should_reload(self):
            return True

        def update_callback(self):
            pass

    yield SomeWatcher


@pytest.mark.parametrize(
    "header, user, method, status, user_name",
    [
        ("X-User", "alice", "GET", 200, "X-User"),
        ("X-USER", "alice", "GET", 200, "x-user"),
        ("x-user", "alice", "GET", 200, "X-USER"),
        ("X-User", "alice", "GET", 200, "X-USER"),
        ("X-User", "alice", "GET", 200, "X-Not-A-Header"),
        ("X-User", "alice", "POST", 201, None),
        ("X-User", "alice", "DELETE", 202, None),
        ("X-User", "bob", "GET", 200, None),
        ("X-User", "bob", "POST", 401, None),
        ("X-User", "bob", "DELETE", 401, None),
        ("X-Idp-Groups", "admin", "GET", 401, "X-User"),
        ("X-Idp-Groups", "group with space, users", "GET", 200, None),
        ("X-Idp-Groups", "noexist,testnoexist,users", "GET", 200, None),
        # ("X-Idp-Groups", "noexist testnoexist users", "GET", 200, None),
        ("X-Idp-Groups", "noexist, testnoexist, users", "GET", 200, None),
        ("X-Idp-Groups", "group with space", "GET", 200, None),
        ("X-Idp-Groups", "somegroup, group with space", "GET", 200, None),
        ("Authorization", "Basic Ym9iOnBhc3N3b3Jk", "GET", 200, "Authorization"),
        (
            "Authorization",
            "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6ImJvYiJ9."
            "LM-CqxAM2MtT2uT3AO69rZ3WJ81nnyMQicizh4oqBwk",
            "GET",
            200,
            None,
        ),
        (
            "Authorization",
            "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJleHAiOjE2MTUxMDg0OTIuNTY5MjksImlkZW50aXR5IjoiQm9iIn0."
            "CAeMpG-gKbucHU7-KMiqM7H_gTkHSRvXSjNtlvh5DlE",
            "GET",
            401,
            None,
        ),
        ("Authorization", "Unsupported Ym9iOnBhc3N3b3Jk", "GET", 401, None),
        ("Authorization", "Unsupported Ym9iOnBhc3N3b3Jk", "GET", 401, None),
    ],
)
def test_enforcer(app_fixture, enforcer, header, user, method, status, user_name):
    # enable auditing with user name
    if user_name:
        enforcer.user_name_headers = {user_name}

    @app_fixture.route("/")
    @enforcer.enforcer
    def index():
        return jsonify({"message": "passed"}), 200

    @app_fixture.route("/item", methods=["GET", "POST", "DELETE"])
    @enforcer.enforcer
    def item():
        if request.method == "GET":
            return jsonify({"message": "passed"}), 200
        elif request.method == "POST":
            return jsonify({"message": "passed"}), 201
        elif request.method == "DELETE":
            return jsonify({"message": "passed"}), 202

    headers = {header: user}
    c = app_fixture.test_client()
    # c.post('/add', data=dict(title='2nd Item', text='The text'))
    rv = c.get("/")
    assert rv.status_code == 401
    caller = getattr(c, method.lower())
    rv = caller("/item", headers=headers)
    assert rv.status_code == status


@pytest.mark.parametrize(
    "header, user, method, status",
    [
        ("X-User", "alice", "GET", 200),
        ("X-User", "alice", "POST", 201),
        ("X-User", "alice", "DELETE", 202),
        ("X-User", "bob", "GET", 200),
        ("X-User", "bob", "POST", 401),
        ("X-User", "bob", "DELETE", 401),
        ("X-Idp-Groups", "admin", "GET", 401),
        ("X-Idp-Groups", "users", "GET", 200),
        ("Authorization", "Basic Ym9iOnBhc3N3b3Jk", "GET", 200),
        ("Authorization", "Unsupported Ym9iOnBhc3N3b3Jk", "GET", 401),
    ],
)
def test_enforcer_with_watcher(
    app_fixture, enforcer, header, user, method, status, watcher
):
    enforcer.set_watcher(watcher())

    @app_fixture.route("/")
    @enforcer.enforcer
    def index():
        return jsonify({"message": "passed"}), 200

    @app_fixture.route("/item", methods=["GET", "POST", "DELETE"])
    @enforcer.enforcer
    def item():
        if request.method == "GET":
            return jsonify({"message": "passed"}), 200
        elif request.method == "POST":
            return jsonify({"message": "passed"}), 201
        elif request.method == "DELETE":
            return jsonify({"message": "passed"}), 202

    headers = {header: user}
    c = app_fixture.test_client()
    # c.post('/add', data=dict(title='2nd Item', text='The text'))
    rv = c.get("/")
    assert rv.status_code == 401
    caller = getattr(c, method.lower())
    rv = caller("/item", headers=headers)
    assert rv.status_code == status


def test_manager(app_fixture, enforcer):
    @app_fixture.route("/manager", methods=["POST"])
    @enforcer.manager
    def manager(manager):
        assert isinstance(manager, Enforcer)
        return jsonify({"message": "passed"}), 201

    c = app_fixture.test_client()
    c.post("/manager")


def test_enforcer_set_watcher(enforcer, watcher):
    assert enforcer.e.watcher is None
    enforcer.set_watcher(watcher())
    assert isinstance(enforcer.e.watcher, watcher)


@pytest.mark.parametrize(
    "owner, method, status",
    [
        (["alice"], "GET", 200),
        (["alice"], "POST", 201),
        (["alice"], "DELETE", 202),
        (["bob"], "GET", 200),
        (["bob"], "POST", 401),
        (["bob"], "DELETE", 401),
        (["admin"], "GET", 401),
        (["users"], "GET", 200),
        (["alice", "bob"], "POST", 201),
        (["noexist", "testnoexist"], "POST", 401),
    ],
)
def test_enforcer_with_owner_loader(app_fixture, enforcer, owner, method, status):
    @app_fixture.route("/")
    @enforcer.enforcer
    def index():
        return jsonify({"message": "passed"}), 200

    @app_fixture.route("/item", methods=["GET", "POST", "DELETE"])
    @enforcer.enforcer
    def item():
        if request.method == "GET":
            return jsonify({"message": "passed"}), 200
        elif request.method == "POST":
            return jsonify({"message": "passed"}), 201
        elif request.method == "DELETE":
            return jsonify({"message": "passed"}), 202

    @enforcer.owner_loader
    def owner_loader():
        return owner

    c = app_fixture.test_client()
    # c.post('/add', data=dict(title='2nd Item', text='The text'))
    rv = c.get("/")
    assert rv.status_code == 401
    caller = getattr(c, method.lower())
    rv = caller("/item")
    assert rv.status_code == status


@pytest.mark.parametrize(
    "header_string, expected_list",
    [
        ("noexist,testnoexist,users  ", ["noexist", "testnoexist", "users"]),
        ("noexist,   testnoexist,   users", ["noexist", "testnoexist", "users"]),
        ("noexist, testnoexist, users", ["noexist", "testnoexist", "users"]),
        ("somegroup, group with space", ["somegroup", "group with space"]),
        ("group with space", ["group with space"]),
        ("group 'with, space", ["group 'with", "space"]),
    ],
)
def test_sanitize_group_headers(header_string, expected_list):
    header_list = CasbinEnforcer.sanitize_group_headers(header_string)
    assert header_list == expected_list


@pytest.mark.parametrize(
    "header_string, expected_list",
    [
        ("noexist testnoexist users  ", ["noexist", "testnoexist", "users"]),
        ("noexist   testnoexist   users", ["noexist", "testnoexist", "users"]),
        ("noexist, testnoexist, users", ["noexist,", "testnoexist,", "users"]),
        ("somegroup, group with space", ["somegroup,", "group", "with", "space"]),
        ('"agroup" "delimited by" "spaces"', ["agroup", "delimited by", "spaces"]),
        ("'agroup' 'delimited by' 'spaces'", ["agroup", "delimited by", "spaces"]),
        ("group'with space", ["group'with", "space"]),
        ("group' with space", ["group'", "with", "space"]),
        (
            "'group with' space",
            ["'group", "with'", "space"],
        ),  # quotes must be used on all groups, not only in 1
        ('"group with space"', ["group with space"]),
        ("'group with space'", ["group with space"]),
        ("group with space", ["group", "with", "space"]),
    ],
)
def test_sanitize_group_headers_with_whitespace(header_string, expected_list):
    header_list = CasbinEnforcer.sanitize_group_headers(header_string, " ")
    assert header_list == expected_list
