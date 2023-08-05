# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json


class HTTPError(Exception):
    """ Base of all other errors"""

    def __init__(self, error):
        self.status_code = error.code
        self.reason = error.reason
        self.body = error.read()
        self.headers = error.hdrs

    @property
    def to_object(self):
        """
        :return: object of response error from the API
        """
        try:
            return json.loads(self.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return {'exception': self.body.decode('utf-8')}

    def __str__(self):
        return self.to_object.get('exception')


class BadRequestsError(HTTPError):
    pass


class UnauthorizedError(HTTPError):
    pass


class ForbiddenError(HTTPError):
    pass


class NotFoundError(HTTPError):
    pass


class MethodNotAllowedError(HTTPError):
    pass


class PayloadTooLargeError(HTTPError):
    pass


class UnsupportedMediaTypeError(HTTPError):
    pass


class TooManyRequestsError(HTTPError):
    pass


class InternalServerError(HTTPError):
    pass


class ServiceUnavailableError(HTTPError):
    pass


class GatewayTimeoutError(HTTPError):
    pass


err_dict = {
    400: BadRequestsError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowedError,
    413: PayloadTooLargeError,
    415: UnsupportedMediaTypeError,
    429: TooManyRequestsError,
    500: InternalServerError,
    503: ServiceUnavailableError,
    504: GatewayTimeoutError,
}


def handle_error(error):
    try:
        exc = err_dict[error.code](error)
    except KeyError:
        return HTTPError(error)
    return exc
