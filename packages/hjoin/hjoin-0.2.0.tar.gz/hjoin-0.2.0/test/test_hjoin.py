#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `hjoin` module.
"""

import pytest
from hjoin import *


def test_string_shape():
    assert string_shape('') == (0, 0)
    assert string_shape('this') == (1, 4)
    assert string_shape('this\nis') == (2, 4)
    assert string_shape('this\nis\n') == (2, 4)
    assert string_shape('this\nis\n\n') == (3, 4)


def test_hjoin_null():
    assert hjoin([]) == ''
    assert hjoin(None) == ''


def test_hjoin_1d():
    assert hjoin(['this']) == 'this'
    assert hjoin(['this', 'that']) == 'this that'
    assert hjoin(['this', 'that', 'and']) == 'this that and'


def test_hjoin_2d():
    assert hjoin(['this\nthing', 'is']) == 'this  is\nthing   '
    assert hjoin(['this\nthing', 'is\ngood']) == 'this  is  \nthing good'
    assert hjoin(['this', 'is\ngood\nenough']) == \
                  'this is    \n     good  \n     enough'
    assert hjoin(['this\nthing', 'is'], sep=' | ') == \
                  'this  | is\nthing |   '


def test_hjoin_ansi():
    from colors import red, blue
    s = red('this perhaps\nand\nthat')
    t = blue('and\none\nmore\nthing')
    result = hjoin([s, t])
    answer = '\x1b[31mthis perhaps\x1b[0m \x1b[34mand\x1b[0m  \n\x1b[31mand\x1b[0m          \x1b[34mone\x1b[0m  \n\x1b[31mthat\x1b[0m         \x1b[34mmore\x1b[0m \n             \x1b[34mthing\x1b[0m'
    assert result == answer
