# -*- coding: utf-8 -*-


class InvalidParameterException(Exception):

    status_code = 400

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.payload = payload
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
