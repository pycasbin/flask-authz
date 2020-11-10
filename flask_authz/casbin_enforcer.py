"""flask-casbin: Flask module for using Casbin with flask apps
"""
import casbin
from flask import request, jsonify
from functools import wraps
from abc import ABC
from abc import abstractmethod

from flask_authz.utils import authorization_decoder, UnSupportedAuthType


class CasbinEnforcer:
    """
    Casbin Enforce decorator
    """

    e = None

    def __init__(self, app, adapter, watcher=None):
        """
        Args:
            app (object): Flask App object to get Casbin Model
            adapter (object): Casbin Adapter
        """
        self.app = app
        self.adapter = adapter
        self.e = casbin.Enforcer(app.config.get("CASBIN_MODEL"), self.adapter, True)
        if watcher:
            self.e.set_watcher(watcher)
        self._owner_loader = None
        self.user_name_headers = app.config.get("CASBIN_USER_NAME_HEADERS", None)

    def set_watcher(self, watcher):
        """
        Set the watcher to use with the underlying casbin enforcer
        Args:
            watcher (object):
        Returns:
            None
        """
        self.e.set_watcher(watcher)

    def owner_loader(self, callback):
        """
        This sets the callback for get owner. The
        function return a owner object, or ``None``

        :param callback: The callback for retrieving a owner object.
        :type callback: callable
        """
        self._owner_loader = callback
        return callback

    def enforcer(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.e.watcher and self.e.watcher.should_reload():
                self.e.watcher.update_callback()
            # String used to hold the owners user name for audit logging
            owner_audit = ""

            # Check sub, obj act against Casbin polices
            self.app.logger.debug(
                "Enforce Headers Config: %s\nRequest Headers: %s"
                % (self.app.config.get("CASBIN_OWNER_HEADERS"), request.headers)
            )
            # Set resource URI from request
            uri = str(request.path)
            # Get owner from owner_loader
            if self._owner_loader:
                self.app.logger.info("Get owner from owner_loader")
                for owner in self._owner_loader():
                    if self.e.enforce(
                            owner.strip('"'), uri, request.method
                    ):
                        return func(*args, **kwargs)
            for header in map(str.lower, self.app.config.get("CASBIN_OWNER_HEADERS")):
                if header in request.headers:
                    # Make Authorization Header Parser standard
                    if header == "authorization":
                        # Get Auth Value then decode and parse for owner
                        try:
                            owner = authorization_decoder(request.headers.get(header))
                        except UnSupportedAuthType:
                            # Continue if catch unsupported type in the event of
                            # Other headers needing to be checked
                            self.app.logger.info(
                                "Authorization header type requested for "
                                "decoding is unsupported by flask-casbin at this time"
                            )
                            continue

                        if self.user_name_headers and header in self.user_name_headers:
                            owner_audit = owner
                        if self.e.enforce(owner, uri, request.method):
                            return func(*args, **kwargs)
                    else:
                        # Split header by ',' in case of groups when groups are
                        # sent "group1,group2,group3,..." in the header
                        for owner in self.sanitize_group_headers(
                            request.headers.get(header)
                        ):
                            self.app.logger.debug(
                                "Enforce against owner: %s header: %s"
                                % (owner.strip('"'), header)
                            )
                            if self.user_name_headers and header in map(str.lower, self.user_name_headers):
                                owner_audit = owner
                            if self.e.enforce(
                                owner.strip('"'), uri, request.method
                            ):
                                return func(*args, **kwargs)
            else:
                self.app.logger.error(
                    "Unauthorized attempt: method: %s resource: %s%s" % (
                        request.method,
                        uri,
                        "" if not self.user_name_headers and owner_audit != "" else " by user: %s" % owner_audit
                    )
                )
                return (jsonify({"message": "Unauthorized"}), 401)

        return wrapper

    @staticmethod
    def sanitize_group_headers(headers_str):
        """
        Sanitizes group header string so that it is easily parsable by enforcer
        removes extra spaces, and converts comma delimited or white space
        delimited list into a list.
        Returns:
            str
        """
        # If there are commas and white space in the string,
        # remove the whitespace
        if " " in headers_str and "," in headers_str:
            headers_str = headers_str.replace(" ", "")
        # If there are no commas in the string, return a list
        # delimited by whitespace
        if " " in headers_str and "," not in headers_str:
            return headers_str.split(" ")
        # There are commas and no whitespace in the string, return a list
        # delimited by commas
        else:
            return headers_str.split(",")

    def manager(self, func):
        """Get the Casbin Enforcer Object to manager Casbin"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self.e, *args, **kwargs)

        return wrapper


class Watcher(ABC):
    """
    Watcher interface as it should be implemented for flask-casbin
    """

    @abstractmethod
    def update(self):
        """
        Watcher interface as it should be implemented for flask-casbin
        Returns:
            None
        """
        pass

    @abstractmethod
    def set_update_callback(self):
        """
        Set the update callback to be used when an update is detected
        Returns:
            None
        """
        pass

    @abstractmethod
    def should_reload(self):
        """
        Method which checks if there is an update necessary for the casbin
        roles. This is called with each flask request.
        Returns:
            Bool
        """
        pass
