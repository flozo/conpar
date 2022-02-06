#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of functions."""

import os


def removespace(line):
    """Remove all spaces from line."""
    return line.replace(' ', '')


def iscomment(line, comment_char):
    """Check if first character (except spaces) is comment character."""
    if len(line) == 0:
        return False
    if line[0] == comment_char:
        return True
    else:
        return False


def isempty(line):
    """Check if line is empty (except spaces)."""
    if line.replace(' ', '') == '':
        return True
    else:
        return False


def iskeyvaluepair(line, key_value_sep):
    """Check if line contains a key-value separator."""
    if key_value_sep in line:
        return True
    else:
        return False


def issection(line, section_marker):
    """Check if line has a section marker."""
    if len(line) == 0:
        return False
    if line[0] == section_marker[0] and line[-1] == section_marker[1]:
        return True
    else:
        return False


class Config_settings:
    """Define configuration settings."""

    def __init__(self, comment_char='#', key_value_sep='=',
                 section_marker=['[', ']']):
        self.comment_char = comment_char
        self.key_value_sep = key_value_sep
        self.section_marker = section_marker


class Configuration(Config_settings):
    """Define configuration settings."""

    def __init__(self, comment_char, key_value_sep, section_marker, rawlines):
        super().__init__(comment_char, key_value_sep, section_marker)
        self.rawlines = rawlines

    def get_types(self, ignore_space):
        """Determine configuration content type."""
        types = []
        for line in self.rawlines:
            if ignore_space is True:
                line = removespace(line)
            if iscomment(line, self.comment_char) is True:
                types.append('comment')
            elif isempty(line) is True:
                types.append('empty')
            elif iskeyvaluepair(line, self.key_value_sep) is True:
                types.append('key_value_pair')
            elif issection(line, self.section_marker) is True:
                types.append('section_head')
            else:
                types.append('unknown')
        return types


def filetolist(inputfile):
    """
    Read file into list line by line.

    Parameters
    ----------
    inputfile : string
        name of input file.

    Returns
    -------
    lines : list of strings
        list of file rows.
    """
    with open(inputfile, 'r', encoding='utf-8') as f:
        lines = []
        for line in f:
            lines.append(line.rstrip())
    return lines


def listtofile(outputfile, lines):
    """
    Write list to file.

    Parameters
    ----------
    outputfile : string
        filename for output.
    listname : list of strings
        list to be written to file.

    Returns
    -------
    None.
    """
    with open(outputfile, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def check_config_dir(config_dir):
    """Check if config directory exists. If not, ask for creating one."""
    if not os.path.isdir(config_dir):
        print('[config] Config directory {} not found.'.format(config_dir))
        create_config_dir = input('[config] Create config directory {} ? '
                                  '(Y/n): '.format(config_dir))
        if create_config_dir == 'Y':
            os.makedirs(config_dir)
            print('[config] Config directory {} created.'.format(config_dir))
        else:
            print('[config] No config directory created.')
