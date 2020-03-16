# Copyright 2019 The Casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sqlite3
from werkzeug.wrappers import Request
from werkzeug.exceptions import Forbidden
from casbin_sqlalchemy_adapter import CasbinRule
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from casbin_sqlalchemy_adapter import Base

class CasbinMiddleware:
    def __init__(self, app, enforcer):
        self.app = app
        self.enforcer = enforcer

    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        request = Request(environ)

        # Check the permission for each request.
        if not self.check_permission(request):
            # Not authorized, return HTTP 403 error.
            return Forbidden()(environ, start_response)

        # Permission passed, go to next module.
        return self.app(environ, start_response)

    def check_permission(self, request):
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()
        # currently it is dummy user but change to the logged in user 
        cur.execute("SELECT * FROM casbin_rule where v0='prince'") 
 
        rows = cur.fetchall()
        print(rows[0][3],rows[0][4])
        # Customize it based on your authentication method.
        user = request.remote_user
        if user is None:
            user = 'prince'
        path = request.path
        method = request.method
	
        return path==rows[0][3] and method==rows[0][4]
