#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test functions for functions.py"""

import conpar.functions as fn


def test_removespace():
    test_lines = [
        '0123456789',
        '     56789',
        '012345    ',
        '    456   ',
        '0123   789',
        ' 1 3 5 7 9',
        '0 2 4 6 8 ',
        '          ',
        '    # Comment  ',
        '  [ section1 ] ',
        ' key = value ',
        ]
    result_lines = [
        '0123456789',
        '56789',
        '012345',
        '456',
        '0123789',
        '13579',
        '02468',
        '',
        '#Comment',
        '[section1]',
        'key=value',
        ]
    for test_line, result_line in zip(test_lines, result_lines):
        assert fn.removespace(test_line) == result_line


def test_iscomment():
    line_iscomment_true = [
        '### Comment',
        '# Comment',
        ]
    line_iscomment_false = [
        ' ### Comment',
        ' # Comment',
        'key = value',
        'key=value',
        '  key = value  ',
        '',
        '          ',
        ]
    for line in line_iscomment_true:
        assert fn.iscomment(line, '#') is True
    for line in line_iscomment_false:
        assert fn.iscomment(line, '#') is False


def test_isempty():
    line_isempty_true = [
        '',
        '          ',
        ]
    line_isempty_false = [
        '0 2 4 6 8 ',
        '### Comment',
        '# Comment',
        ' # Comment',
        '[section1]',
        'key = value',
        ]
    for line in line_isempty_true:
        assert fn.isempty(line) is True
    for line in line_isempty_false:
        assert fn.isempty(line) is False


def test_iskeyvaluepair():
    line_iskeyvaluepair_true = [
        'key = value',
        'key=value',
        '  key = value  ',
        'asljfjdjfljl=lkjasdjfjj',
        ]
    line_iskeyvaluepair_false = [
        'keyvalue',
        '',
        'key:value',
        '            ',
        ]
    for line in line_iskeyvaluepair_true:
        assert fn.iskeyvaluepair(line, '=') is True
    for line in line_iskeyvaluepair_false:
        assert fn.iskeyvaluepair(line, '=') is False


def test_issection():
    line_issection_true = [
        '[section1]',
        '[[[section1]]]',
        '[]ction1[]]',
        ]
    line_issection_false = [
        '### Comment',
        '# Comment',
        ' # Comment',
        ']section1[',
        'key = value',
        '',
        '          ',
        ]
    for line in line_issection_true:
        assert fn.issection(line, ['[', ']']) is True
    for line in line_issection_false:
        assert fn.issection(line, ['[', ']']) is False


def test_gettypes():
    lines = [
        '# This is a comment.',
        '# This is another comment.',
        '',
        '[section1]',
        'key1 = value1',
        'key2 = value2',
        'key3 = value3',
        '',
        '',
        '# This is also a comment.',
        '',
        '[section2]',
        'key1 = value1',
        'key2 = value2',
        'key3 = value3',
        'aklwfwiopwjj',
        '',
        ]
    types = [
        'comment',
        'comment',
        'empty',
        'section_head',
        'key_value_pair',
        'key_value_pair',
        'key_value_pair',
        'empty',
        'empty',
        'comment',
        'empty',
        'section_head',
        'key_value_pair',
        'key_value_pair',
        'key_value_pair',
        'unknown',
        'empty',
        ]
    cfg1 = fn.Configuration('#', '=', ['[', ']'], lines)
    assert cfg1.get_types(True) == types
