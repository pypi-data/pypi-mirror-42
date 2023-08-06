# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import copy
import hashlib

from pywe_utils import to_binary, to_text


__all__ = ['format_url', 'calculate_signature', 'check_signature', 'fill_signature']


def format_url(params, api_key=None):
    data = [to_binary('{0}={1}'.format(k, params[k])) for k in sorted(params) if params[k]]
    data = b'&'.join(data)
    if api_key:
        data += to_binary('{0}'.format(api_key))
    return data


# Toutiao Relative Signature Algorithm
#   See: https://developer.toutiao.com/docs/payment/#%E7%AD%BE%E5%90%8D%E8%AF%B4%E6%98%8E

def calculate_signature(params, api_key):
    url = format_url(params, api_key)
    return to_text(hashlib.md5(url).hexdigest())


def check_signature(params, api_key, sign=None):
    _params = copy.deepcopy(params)
    sign = sign or _params.pop('sign', '')
    return sign == calculate_signature(_params, api_key)


def fill_signature(params, api_key):
    sign = calculate_signature(params, api_key)
    params['sign'] = sign
    return params
