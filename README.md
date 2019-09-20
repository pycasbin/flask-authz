flask-casbin
===============================

A Flask Casbin interface that allows you to decorate routes

Installation / Usage
--------------------

To install use pip:
```
$ pip install flask-casbin
```

Or clone the repo:
```
$ git clone https://github.com/sciencelogic/flask-casbin.git
$ python setup.py install
```

Module Usage:
```python
app = Flask(__name__)
# Set up Casbin model config
app.config['CASBIN_MODEL'] = 'casbinmodel.conf'
# Set headers where owner for enforcement policy should be located
app.config['CASBIN_OWNER_HEADERS'] = {'X-User', 'X-Group'}
# Set up Casbin Adapter
adapter = casbin_couchbase_adapter.Adapter(...)
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

Development
------------
1. Fork
2. Install Dev ENV
```python
# Install Flask-Casbin with Dev packages
pip install -r dev_requirements.txt
pip install -r requirements.txt
pip install -e .
# Install Pre-commits
pre-commit install
# Create feature branch
git checkout -b feature-more-cool-stuff
# Code stuff
```
Then push your changes and create a PR


