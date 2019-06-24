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

from werkzeug.wrappers import Request
from werkzeug.exceptions import Forbidden


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
        # Customize it based on your authentication method.
        user = request.remote_user
        if user is None:
            user = 'anonymous'
        path = request.path
        method = request.method
        return self.enforcer.enforce(user, path, method)
