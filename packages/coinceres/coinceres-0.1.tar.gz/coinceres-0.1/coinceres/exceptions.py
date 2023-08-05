# -*- coding: utf-8 -*-
from functools import wraps


def error_helper(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        r = f(*args, **kwargs)
        data = r.json()
        if r.status_code != 200:
            raise ValueError(data.get('message'))
        if data.get('code') is None:
            return data
        if data.get('code') != '200':
            raise ValueError(data.get('message'))
        return data.get('data')
    return _wrapper
