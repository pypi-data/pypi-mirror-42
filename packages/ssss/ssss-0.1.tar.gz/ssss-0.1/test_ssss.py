# coding: utf-8

from os import urandom
from random import randint
from unittest import TestCase

import ssss


class TestSSSS(TestCase):
    def test_symmetric(self):
        for _ in range(10):
            n = randint(3, 100)
            r = randint(1, n)
            secret = urandom(32)
            frags = ssss.split(secret, n, r)
            recovered = ssss.combine(r, frags[:r])
            self.assertEqual(secret, recovered)
