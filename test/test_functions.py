#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test functions for functions.py"""

import conpar.functions as fn


def test_is_comment():
    line_iscomment_true = [
        '### Comment',
        '# Comment',
        '# Comment     adfsdgs  ',
        ' ### Comment',
        ' # Comment',
        ]
    line_iscomment_false = [
        'key = value',
        'key=value',
        '  key = value  ',
        '[section]',
        '  [  section  ]  ',
        '',
        '          ',
        ]
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    for line in line_iscomment_true:
        assert fn.Line(line, **cfg).is_comment() is True
    for line in line_iscomment_false:
        assert fn.Line(line, **cfg).is_comment() is False


def test_is_empty():
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
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    for line in line_isempty_true:
        assert fn.Line(line, **cfg).is_empty() is True
    for line in line_isempty_false:
        assert fn.Line(line, **cfg).is_empty() is False


def test_is_key_value_pair():
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
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    for line in line_iskeyvaluepair_true:
        assert fn.Line(line, **cfg).is_key_value_pair() is True
    for line in line_iskeyvaluepair_false:
        assert fn.Line(line, **cfg).is_key_value_pair() is False


def test_is_section():
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
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    for line in line_issection_true:
        assert fn.Line(line, **cfg).is_section() is True
    for line in line_issection_false:
        assert fn.Line(line, **cfg).is_section() is False


def test_is_unknown():
    line_is_unknown_true = [
        'sakjflkjgl',
        'lkajlkfj   lkdjlfk',
        ']section1[',
        'aljfljdfj # comment',
        ]
    line_is_unknown_false = [
        '### Comment',
        '# Comment',
        '# Comment     adfsdgs  ',
        ' ### Comment',
        ' # Comment',
        '',
        '          ',
        'key = value',
        'key=value',
        '  key = value  ',
        'asljfjdjfljl=lkjasdjfjj',
        '[section1]',
        '[[[section1]]]',
        '[]ction1[]]',
        ]
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    for line in line_is_unknown_true:
        assert fn.Line(line, **cfg).is_unknown() is True
    for line in line_is_unknown_false:
        assert fn.Line(line, **cfg).is_unknown() is False


def test_comment():
    line_comments_raw = [
        '# comment1',
        '   # comment2',
        '# comment3     ',
        '  #    comment4    ',
        '#   comment comment 5   ',
        ]
    line_comments_content = [
        'comment1',
        'comment2',
        'comment3',
        'comment4',
        'comment comment 5',
        ]
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    for line_in, line_out in zip(line_comments_raw, line_comments_content):
        assert fn.Line(line_in, **cfg).comment() == line_out


def test_section_name():
    line_section_name_raw = [
        '[section1]',
        '   [section2]',
        '[section3]     ',
        '    [section4]    ',
        '   [    section5    ]  ',
        '  [  section name 6     ]   ',
        ]
    line_section_name_content = [
        'section1',
        'section2',
        'section3',
        'section4',
        'section5',
        'section name 6',
        ]
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    for line_in, line_out in zip(line_section_name_raw,
                                 line_section_name_content):
        assert fn.Line(line_in, **cfg).section_name() == line_out


def test_key_value_pair():
    line_key_value_raw = [
        'key1=value1',
        'key2 = value2',
        '   key3    =     value3    ',
        '   key key key 4   =  value value value 4  ',
        ]
    line_key_value_content = [
        ('key1', 'value1'),
        ('key2', 'value2'),
        ('key3', 'value3'),
        ('key key key 4', 'value value value 4'),
        ]
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    for line_in, line_out in zip(line_key_value_raw, line_key_value_content):
        assert fn.Line(line_in, **cfg).key_value_pair() == line_out


def test_get_types():
    rawlines = [
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
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    assert fn.Configuration(rawlines, **cfg).get_types() == types


def test_get_content():
    rawlines = [
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
    content = [
        'This is a comment.',
        'This is another comment.',
        '',
        'section1',
        ('key1', 'value1'),
        ('key2', 'value2'),
        ('key3', 'value3'),
        '',
        '',
        'This is also a comment.',
        '',
        'section2',
        ('key1', 'value1'),
        ('key2', 'value2'),
        ('key3', 'value3'),
        'aklwfwiopwjj',
        '',
        ]
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    assert fn.Configuration(rawlines, **cfg).get_content() == content


def test_formatted():
    rawlines = [
        '#This is a comment.',
        '  # This is another comment.   ',
        '',
        '   [   section1    ]    ',
        'key1 = value1',
        'key2=value2',
        '   key key key 3 =     value value 3   ',
        '',
        'aklwfwiopwjj',
        ]
    formatted = [
        '# This is a comment.',
        '# This is another comment.',
        '',
        '[ section1 ]',
        'key1 = value1',
        'key2 = value2',
        'key key key 3 = value value 3',
        '',
        'aklwfwiopwjj',
        ]
    cfg = {'comment_char': '#',
           'section_marker': '[]',
           'assignment_char': '=',
           }
    assert fn.Configuration(rawlines, **cfg).formatted() == formatted
