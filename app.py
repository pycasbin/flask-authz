from authz.middleware import CasbinMiddleware
import casbin_sqlalchemy_adapter
from casbin_sqlalchemy_adapter import Adapter
from casbin_sqlalchemy_adapter import Base
from casbin_sqlalchemy_adapter import CasbinRule
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest import TestCase
import casbin
import os
from flask import Flask

def get_fixture(path):
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + path)

def get_enforcer():
    engine = create_engine("sqlite:///test.db")
    # engine = create_engine('sqlite:///' + os.path.split(os.path.realpath(__file__))[0] + '/test.db', echo=True)
    adapter = Adapter(engine)

    return casbin.Enforcer(get_fixture('rbac_model.conf'), adapter)

app = Flask(__name__)

# Initialize the Casbin enforcer, load the casbin model and policy from files.
# Change the 2nd arg to use a database.
enforcer = get_enforcer()

app.wsgi_app = CasbinMiddleware(app.wsgi_app, enforcer)


@app.route("/")
def hello_world():
    # ("anonymous", "/", "GET") ==> True, so return HTTP 200.
    return "Hello World!"


@app.route('/data')
def data():
    # ("anonymous", "/data", "GET") ==> False, so return HTTP 403.
    return "data"


if __name__ == '__main__':
    app.run(debug=True)
