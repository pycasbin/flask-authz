# flask-authz

[![GitHub Action](https://github.com/pycasbin/flask-authz/workflows/build/badge.svg?branch=master)](https://github.com/pycasbin/flask-authz/actions)
[![Coverage Status](https://coveralls.io/repos/github/pycasbin/flask-authz/badge.svg)](https://coveralls.io/github/pycasbin/flask-authz)
[![Version](https://img.shields.io/pypi/v/flask-authz.svg)](https://pypi.org/project/flask-authz/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/flask-authz.svg)](https://pypi.org/project/flask-authz/)
[![Pyversions](https://img.shields.io/pypi/pyversions/flask-authz.svg)](https://pypi.org/project/flask-authz/)
[![Download](https://img.shields.io/pypi/dm/flask-authz.svg)](https://pypi.org/project/flask-authz/)
[![Discord](https://img.shields.io/discord/1022748306096537660?logo=discord&label=discord&color=5865F2)](https://discord.gg/S5UjpzGZjN)

flask-authz is an authorization middleware for [Flask](http://flask.pocoo.org/), it's based on [PyCasbin](https://github.com/casbin/pycasbin).

## Installation

```
pip install flask-authz
```
Or clone the repo:
```
$ git clone https://github.com/pycasbin/flask-authz.git
$ python setup.py install
```

Module Usage:
```python
from flask import Flask
from flask_authz import CasbinEnforcer
from casbin.persist.adapters import FileAdapter

app = Flask(__name__)
# Set up Casbin model config
app.config['CASBIN_MODEL'] = 'casbinmodel.conf'
# Set headers where owner for enforcement policy should be located
app.config['CASBIN_OWNER_HEADERS'] = {'X-User', 'X-Group'}
# Add User Audit Logging with user name associated to log
# i.e. `[2020-11-10 12:55:06,060] ERROR in casbin_enforcer: Unauthorized attempt: method: GET resource: /api/v1/item by user: janedoe@example.com`
app.config['CASBIN_USER_NAME_HEADERS'] = {'X-User'}
# Set up Casbin Adapter
adapter = FileAdapter('rbac_policy.csv')
casbin_enforcer = CasbinEnforcer(app, adapter)

@app.route('/', methods=['GET'])
@casbin_enforcer.enforcer
def get_root():
    return jsonify({'message': 'If you see this you have access'})

@app.route('/manager', methods=['POST'])
@casbin_enforcer.enforcer
@casbin_enforcer.manager
def make_casbin_change(manager):
    # Manager is an casbin.enforcer.Enforcer object to make changes to Casbin
    return jsonify({'message': 'If you see this you have access'})
```
Example Config
This example file can be found in `tests/casbin_files`
```ini
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = (p.sub == "*" || g(r.sub, p.sub)) && r.obj == p.obj && (p.act == "*" || r.act == p.act)
```
Example Policy
This example file can be found in `tests/casbin_files`
```csv
p, alice, /dataset1/*, GET
p, alice, /dataset1/resource1, POST
p, bob, /dataset2/resource1, *
p, bob, /dataset2/resource2, GET
p, bob, /dataset2/folder1/*, POST
p, dataset1_admin, /dataset1/*, *
p, *, /login, *

p, anonymous, /, GET

g, cathy, dataset1_admin
```

Development
------------

#### Run unit tests
1. Fork/Clone repository
2. Install flask-authz dependencies, and run `pytest`
```python
pip install -r dev_requirements.txt
pip install -r requirements.txt
pytest
```

#### Setup pre-commit checks
```python
pre-commit install
```


#### update requirements with pip-tools
```bash
# update requirements.txt
pip-compile --no-annotate --no-header --rebuild requirements.in
# sync venv
pip-sync
```

#### Manually Bump Version
```
bumpversion major  # major release
or
bumpversion minor  # minor release
or
bumpversion patch  # hotfix release
```

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

