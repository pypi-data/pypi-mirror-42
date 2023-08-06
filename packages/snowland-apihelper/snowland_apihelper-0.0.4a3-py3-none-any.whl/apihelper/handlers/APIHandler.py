#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: APIHandler.py
# @time: 2019/1/11 10:43
# @Software: PyCharm

from tornado.web import authenticated
from apihelper.thirdparty.tornado_json.requesthandlers import BaseHandler as Base
from jsonschema import ValidationError
from apihelper.util.jsend import JSendMixin
from apihelper.thirdparty.tornado_json.exceptions import APIError


class BaseHandler(Base):
    """解决JS跨域请求问题"""
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def get_current_user(self):
        return self.get_secure_cookie("apihelper_username")

class APIHandler(BaseHandler, JSendMixin):
    """RequestHandler for API calls

    - Sets header as ``application/json``
    - Provides custom write_error that writes error back as JSON \
    rather than as the standard HTML template
    """

    def initialize(self):
        """
        - Set Content-type for JSON
        """
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):
        """Override of RequestHandler.write_error

        Calls ``error()`` or ``fail()`` from JSendMixin depending on which
        exception was raised with provided reason and status code.

        :type  status_code: int
        :param status_code: HTTP status code
        """
        def get_exc_message(exception):
            return exception.log_message if \
                hasattr(exception, "log_message") else str(exception)

        self.clear()
        self.set_status(status_code)

        # Any APIError exceptions raised will result in a JSend fail written
        # back with the log_message as data. Hence, log_message should NEVER
        # expose internals. Since log_message is proprietary to HTTPError
        # class exceptions, all exceptions without it will return their
        # __str__ representation.
        # All other exceptions result in a JSend error being written back,
        # with log_message only written if debug mode is enabled
        exception = kwargs["exc_info"][1]
        if any(isinstance(exception, c) for c in [APIError, ValidationError]):
            # ValidationError is always due to a malformed request
            if isinstance(exception, ValidationError):
                self.set_status(400)
            self.fail(get_exc_message(exception))
        else:
            self.error(
                message=self._reason,
                data=get_exc_message(exception) if self.settings.get("debug")
                else None,
                code=status_code
            )


# 以下部分参考 https://blog.csdn.net/midion9/article/details/51332973

class LoginHandler(APIHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        cookie_name = self.get_argument('cookiename', 'apihelper_username')

        self.set_secure_cookie(cookie_name, "yes you can!")
        self.success('login successfully')

class WelcomeHandler(APIHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.success('Welcome, {}'.format(self.current_user))


class LogoutHandler(APIHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie("apihelper_username")
        self.success('logout successfully')
