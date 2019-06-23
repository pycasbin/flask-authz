# flask-authz

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/casbin/lobby)

flask-authz is an authorization middleware for [Flask](http://flask.pocoo.org/), it's based on [PyCasbin](https://github.com/casbin/pycasbin).

## Installation

```
pip install flask-authz
```

## Simple Example

This repo is just a working Flask app that shows the usage of flask-authz. To use it in your existing Flask app, you need:

```python
from authz.middleware import CasbinMiddleware
import casbin
from flask import Flask

app = Flask(__name__)

# Initialize the Casbin enforcer, load the casbin model and policy from files.
# Change the 2nd arg to use a database.
enforcer = casbin.Enforcer("authz_model.conf", "authz_policy.csv")

app.wsgi_app = CasbinMiddleware(app.wsgi_app, enforcer)


@app.route("/")
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
```

- The default policy ``authz_policy.csv`` is:

```csv
p, anonymous, /, GET
p, admin, *, *
g, alice, admin
```

It means ``anonymous`` user can only access homepage ``/``. Admin users like alice can access any pages. Currently all accesses are regarded as ``anonymous``. Add your authentication to let a user log in.

## How are subject, object, action defined?

In ``middleware.py``:

```python
def check_permission(self, request):
    # change the user, path, method as you need.
    user = request.remote_user # subject
    if user is None:
        user = 'anonymous'
    path = request.path # object
    method = request.method # action
    return self.enforcer.enforce(user, path, method)
```

You may need to copy the ``middleware.py`` code to your project and modify it directly if you have other definitions for subject, object, action.

## Documentation

The authorization determines a request based on ``{subject, object, action}``, which means what ``subject`` can perform what ``action`` on what ``object``. In this plugin, the meanings are:

1. ``subject``: the logged-in user name
2. ``object``: the URL path for the web resource like "dataset1/item1"
3. ``action``: HTTP method like GET, POST, PUT, DELETE, or the high-level actions you defined like "read-file", "write-blog"

For how to write authorization policy and other details, please refer to [the Casbin's documentation](https://casbin.org).

## Getting Help

- [Casbin](https://casbin.org)

## License

This project is under Apache 2.0 License. See the [LICENSE](LICENSE) file for the full license text.
