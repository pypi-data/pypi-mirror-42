from __future__ import absolute_import, division, print_function


class APIError(Exception):
    '''RGB Notes API Error base class'''
    def __init__(self, message=None, http_body=None,
                 headers=None, code=None):

        super(APIError, self).__init__(message)

        self._message = message
        self.http_body = http_body
        self.headers = headers or {}
        self.code = code

    def __str__(self):
        msg = self._message or "<empty message>"
        return msg

    def __repr__(self):
        return '%s(message=%r)' % (
            self.__class__.__name__,
            self._message)


class InvalidRequestError(APIError):
    def __init__(self, message, http_body=None,
             headers=None, code=None):
        super(InvalidRequestError, self).__init__(message, http_body,
                                                  headers, code)


class AuthenticationError(APIError):
    def __init__(self, message, http_body=None,
                 headers=None, code=None):
            super(AuthenticationError, self).__init__(message, http_body,
                                                      headers, code)
