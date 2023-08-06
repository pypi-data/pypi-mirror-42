#!/usr/bin/env python3
# coding: utf-8
import re
from .prefix_numbers import phone_number_prefixes

__author__ = 'ytyng'
__version__ = '0.1.0'
__license__ = 'BSD'


class PhoneNumberJPError(Exception):
    pass


class PhoneNumberIsNotDigits(PhoneNumberJPError):
    pass


class UnexpectedIndex(PhoneNumberJPError):
    pass


class PrefixNoMatch(PhoneNumberJPError):
    pass


prefix_regex_patterns = [
    {
        'pattern': re.compile('^0(2|[5-9])0'),
        'prefix_digits': 3,
    },
    {
        'pattern': re.compile('^0(120|800|990|570)'),
        'prefix_digits': 4,
    },
]


def _split_tail(prefix, tail):
    # 残りが7桁の場合、3, 4 で分割
    tail_split_digits = int(len(tail) / 2)

    return prefix, tail[:tail_split_digits], tail[tail_split_digits:]


def split_phone_number(phone_number: str):
    if not phone_number.isdigit():
        raise PhoneNumberIsNotDigits(phone_number)

    for p in prefix_regex_patterns:
        if p['pattern'].match(phone_number):
            return _split_tail(phone_number[:p['prefix_digits']],
                               phone_number[p['prefix_digits']:])

    index = phone_number[:2]
    if index not in phone_number_prefixes:
        raise UnexpectedIndex(index)

    for prefix in phone_number_prefixes[index]:
        if phone_number.startswith(prefix):
            prefix_len = len(prefix)
            return _split_tail(phone_number[:prefix_len],
                               phone_number[prefix_len:])

    raise PrefixNoMatch(phone_number)
