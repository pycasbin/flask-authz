# Copyright 2019 The Casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from authz.middleware import CasbinMiddleware
import casbin
from flask import Flask
import os
import unittest

app = Flask(__name__)


def get_example_file(path):
    examples_path = os.path.split(os.path.realpath(__file__))[0] + "/../tests/"
    return os.path.abspath(examples_path + path)


# Initialize the Casbin enforcer, executed only on once.
e = casbin.Enforcer(get_example_file('authz_model.conf'), get_example_file('authz_policy.csv'))

app.wsgi_app = CasbinMiddleware(app.wsgi_app, e)


# All URLs return 200 OK as an example.
@app.errorhandler(404)
def page_not_found(e):
    return '200 OK'

# Start a normal application like this:
# if __name__ == '__main__':
#     app.run()


class TestMiddleware(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def authz_request(self, user, path, method, code):
        rv = None
        if method == 'GET':
            rv = self.app.get(path, environ_base={'REMOTE_USER': user})
        elif method == 'POST':
            rv = self.app.post(path, environ_base={'REMOTE_USER': user})
        elif method == 'DELETE':
            rv = self.app.delete(path, environ_base={'REMOTE_USER': user})

        if code == 200:
            assert rv.status == '200 OK'
        elif code == 403:
            assert rv.status == '403 FORBIDDEN'

    def test_basic(self):
        self.authz_request('alice', '/dataset1/resource1', 'GET', 200)
        self.authz_request('alice', '/dataset1/resource1', 'POST', 200)
        self.authz_request('alice', '/dataset1/resource2', 'GET', 200)
        self.authz_request('alice', '/dataset1/resource2', 'POST', 403)
        self.authz_request('alice', '/login', 'GET', 200)
        self.authz_request('bob', '/login', 'POST', 200)
        self.authz_request('cathy', '/login', 'DELETE', 200)

    def test_path_wildard(self):
        self.authz_request('bob', '/dataset2/resource1', 'GET', 200)
        self.authz_request('bob', '/dataset2/resource1', 'POST', 200)
        self.authz_request('bob', '/dataset2/resource1', 'DELETE', 200)
        self.authz_request('bob', '/dataset2/resource2', 'GET', 200)
        self.authz_request('bob', '/dataset2/resource2', 'POST', 403)
        self.authz_request('bob', '/dataset2/resource2', 'DELETE', 403)

        self.authz_request('bob', '/dataset2/folder1/item1', 'GET', 403)
        self.authz_request('bob', '/dataset2/folder1/item1', 'POST', 200)
        self.authz_request('bob', '/dataset2/folder1/item1', 'DELETE', 403)
        self.authz_request('bob', '/dataset2/folder1/item2', 'GET', 403)
        self.authz_request('bob', '/dataset2/folder1/item2', 'POST', 200)
        self.authz_request('bob', '/dataset2/folder1/item2', 'DELETE', 403)

    # def test_rbac(self):
    #     # cathy can access all /dataset1/* resources via all methods because it has the dataset1_admin role.
    #     self.authz_request('cathy', '/dataset1/item', 'GET', 200)
    #     self.authz_request('cathy', '/dataset1/item', 'POST', 200)
    #     self.authz_request('cathy', '/dataset1/item', 'DELETE', 200)
    #     self.authz_request('cathy', '/dataset2/item', 'GET', 403)
    #     self.authz_request('cathy', '/dataset2/item', 'POST', 403)
    #     self.authz_request('cathy', '/dataset2/item', 'DELETE', 403)
    #
    #     # delete all roles on user cathy, so cathy cannot access any resources now.
    #     e.deleteRolesForUser('cathy')
    #
    #     self.authz_request('cathy', '/dataset1/item', 'GET', 403)
    #     self.authz_request('cathy', '/dataset1/item', 'POST', 403)
    #     self.authz_request('cathy', '/dataset1/item', 'DELETE', 403)
    #     self.authz_request('cathy', '/dataset2/item', 'GET', 403)
    #     self.authz_request('cathy', '/dataset2/item', 'POST', 403)
    #     self.authz_request('cathy', '/dataset2/item', 'DELETE', 403)
