"""flask-casbin: Flask module for using Casbin with flask apps
"""
import casbin
from flask import request, jsonify
from functools import wraps


class CasbinEnforcer:
    """
    Casbin Enforce decorator
    """
    e = None

    def __init__(self, app, adapter):
        """
        Args:
            app (object): Flask App object to get Casbin Model
            adapter (object): Casbin Adapter
        """
        self.app = app
        self.adapter = adapter
        self.e = casbin.Enforcer(
            app.config.get('CASBIN_MODEL'),
            self.adapter,
            True
        )

    def enforcer(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check sub, obj act against Casbin polices
            for header in self.app.config.get('CASBIN_OWNER_HEADERS'):
                if request.headers.has_key(header):
                    for owner in request.headers.getlist(header):
                        self.app.logger.debug(
                            "Enforce against owner: %s header: %s" % (owner, header)
                        )
                        if self.e.enforce(
                            owner,
                            str(request.url_rule),
                            request.method
                        ):
                            return func(*args, **kwargs)
            else:
                return (
                    jsonify({'message': 'Unauthorized'}), 401)

        return wrapper

    def manager(self, func):
        """Get the Casbin Enforcer Object to manager Casbin"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self.e, *args, **kwargs)

        return wrapper

