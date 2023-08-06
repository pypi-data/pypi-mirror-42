#!/usr/bin/env python3
# coding: utf-8
from .prefix_numbers import phone_number_prefixes

__author__ = 'ytyng'
__version__ = '0.2.0'
__license__ = 'BSD'

MAX_PREFIX_DIGIT = 5
MIN_PREFIX_DIGIT = 2


class PhoneNumberJPError(Exception):
    pass


class PhoneNumberIsNotDigits(PhoneNumberJPError):
    pass


class UnexpectedIndex(PhoneNumberJPError):
    pass


class PrefixNoMatch(PhoneNumberJPError):
    pass


def _split_tail(prefix, tail):
    # 残りが7桁の場合、3, 4 で分割
    tail_split_digits = int(len(tail) / 2)

    return prefix, tail[:tail_split_digits], tail[tail_split_digits:]


def split_phone_number(phone_number: str):
    if not phone_number.isdigit():
        raise PhoneNumberIsNotDigits(phone_number)

    for d in range(MAX_PREFIX_DIGIT, MIN_PREFIX_DIGIT - 1, -1):
        p = phone_number[:d]
        if p in phone_number_prefixes[d]:
            return _split_tail(p, phone_number[d:])

    raise PrefixNoMatch(phone_number)
