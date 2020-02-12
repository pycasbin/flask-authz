from authz.middleware import CasbinMiddleware
import casbin
from flask import Flask

app = Flask(__name__)

# Initialize the Casbin enforcer, load the casbin model and policy from files.
# Change the 2nd arg to use a database.
enforcer = casbin.Enforcer("tests/authz_model.conf", "tests/authz_policy.csv")

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
    app.run()
