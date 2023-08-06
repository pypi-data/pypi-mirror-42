#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from persis.persis import fib

__author__ = "Martin Skarzynski"
__copyright__ = "Martin Skarzynski"
__license__ = "MIT"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
