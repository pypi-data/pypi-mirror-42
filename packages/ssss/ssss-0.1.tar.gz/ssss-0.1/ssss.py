# coding: utf-8
# ssss -- Pure Python Shamir's secret sharing scheme implementation
# Copyright (C) 2015-2019 Sergey Matveev <stargrave@stargrave.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
""" Shamir's secret sharing scheme implementation.

https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
"""

from os import urandom

from pygost.utils import bytes2long
from pygost.utils import long2bytes


SECRET_LEN = 32
POLY = 115792089237316195423570985008687907853269984665640564039457584007913129640997  # pylint: disable=line-too-long


def _lshift(x, bits):
    return x * (1 << bits)


def _field_mult(x, y):
    b = x
    z = b if y & 1 == 1 else 0
    for i in range(1, SECRET_LEN * 8):
        b = _lshift(b, 1)
        if (b >> (SECRET_LEN * 8)) & 1 == 1:
            b ^= POLY
        if y & (1 << i):
            z ^= b
    return z


def _horner(t, x, coef):
    y = coef[t - 1]
    for i in range(t - 1, 0, -1):
        y = _field_mult(y, x)
        y ^= coef[i - 1]
    return y


def _field_invert(x):
    u, v = x, POLY
    g, z = 0, 1
    while u > 1:
        i = len(bin(u)[2:]) - len(bin(v)[2:])
        if i < 0:
            u, v = v, u
            z, g = g, z
            i = -i
        u = u ^ _lshift(v, i)
        z = z ^ _lshift(g, i)
    return z


def _calculate_li0(t, x, i):
    li0 = 1
    for j in range(t):
        if j == i:
            continue
        li0 = _field_mult(li0, x[j])
        li0 = _field_mult(li0, _field_invert(x[i] ^ x[j]))
    return li0


def split(secret, n, t):
    """ Split the secret

    :param secret: secret needed to be splitted
    :type secret: str, <=32 bytes
    :param n: number of parts
    :type n: int
    :param t: number of necessary for recovery parts
    :type t: int
    :return: secret's parts
    :rtype: list(tuple(int, str))
    """
    coef = [bytes2long(secret[::-1])]
    if n < 0 or t < 0 or n < t or not secret:
        raise ValueError("Invalid parameters specified")
    for i in range(1, t):
        coef.append(bytes2long(urandom(SECRET_LEN)))
    out = []
    for i in range(1, n + 1):
        out.append((i, long2bytes(_horner(t, i, coef))[::-1]))
    return out


def combine(t, parts):
    """ Combine the secret from the parts

    :param t: number of necessary for recovery parts
    :type t: int
    :param parts: list of parts
    :type parts: similar that *split()* function returns
    :return: recovered secret
    :rtype: str, 32 bytes

    If secret was shorter than 32 bytes, then zeros appended as a pad.
    """
    if t <= 0 or not parts:
        raise ValueError("Invalid parameters specified")
    if len(parts) != len(set(s[1] for s in parts)):
        raise ValueError("Equal parts found")
    x, y = list(zip(*[(s[0], bytes2long(s[1][::-1])) for s in parts]))
    sec = 0
    for i in range(t):
        li0 = _calculate_li0(t, x, i)
        li0si = _field_mult(li0, y[i])
        sec = sec ^ li0si
    return long2bytes(sec)[::-1]
