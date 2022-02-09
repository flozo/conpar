#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of functions."""

import os
import pandas as pd


class Config_settings:
    """Define configuration settings."""

    def __init__(self, comment_char='#', section_marker='[]',
                 key_value_sep='='):
        self.comment_char = comment_char
        self.section_marker = section_marker
        self.key_value_sep = key_value_sep


class Line(Config_settings):
    """Define line properties and methods."""

    def __init__(self, rawline, comment_char, section_marker, key_value_sep):
        super().__init__(comment_char, section_marker, key_value_sep)
        self.rawline = rawline
        # Create a version of rawline without leading and trailing spaces
        self.line = self.rawline.strip()

    def is_comment(self):
        """Check if line is a comment line."""
        # Return False if line is empty
        if len(self.line) == 0:
            return False
        # Check if first character is a comment character
        if self.line[0] == self.comment_char:
            return True
        else:
            return False

    def is_empty(self):
        """Check if line is empty (except spaces)."""
        if self.line.replace(' ', '') == '':
            return True
        else:
            return False

    def is_key_value_pair(self):
        """Check if line contains a key-value separator."""
        if self.key_value_sep in self.line:
            return True
        else:
            return False

    def is_section(self):
        """Check if line has a section marker."""
        # Return False if line is empty
        if len(self.line) == 0:
            return False
        # Return False if first character is not a section marker
        if self.line[0] != self.section_marker[0]:
            return False
        # Check if an optional closing marker is present
        if len(self.section_marker) == 2 and self.line[-1] == self.section_marker[1]:
            return True
        else:
            return False

    def is_unknown(self):
        """Check if line type is unknown."""
        if not(self.is_comment() or self.is_empty() or self.is_key_value_pair() or self.is_section()):
            return True
        else:
            return False

    def comment(self):
        """If line is comment, return comment content."""
        # Check if line is comment
        if self.is_comment() is True:
            # Return comment string without leading and trailing spaces
            return self.line.replace('#', '').strip()

    def key_value_pair(self):
        """If line is a key-value pair, return tuple (key, value)."""
        # Check if line is a key-value pair
        if self.is_key_value_pair() is True:
            # Return key and value strings without leading and trailing spaces
            return (self.line.split(self.key_value_sep)[0].strip(),
                    self.line.split(self.key_value_sep)[1].strip(),)

    def section_name(self):
        """If line is section head, return section name."""
        # Check if line is a section head
        if self.is_section() is True:
            # Return section name without leading and trailing spaces
            return self.line[1:-1].strip()


# def type_definitions():
#     type_defs = {
#         'type_name': ['section_head', 'comment', 'key_value_pair', 'empty'],
#         'marker': ['[', '#', '=', ''],
#         'regex_all': ['\[.*\]', ],
#         'regex_content':,
#         }


class Configuration(Config_settings):
    """Define configuration settings."""

    def __init__(self, rawlines, comment_char, section_marker, key_value_sep):
        super().__init__(comment_char, section_marker, key_value_sep)
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


def config_dict(rawlines, types):
    cfg_dict = {
        'type': types,
        'content': rawlines
        }
    cfg_df = pd.DataFrame(cfg_dict)
    print(cfg_df)
    # regexes = {
    #     'section_head': r'^\s*\[\s*(\S*)\s*\]\s*$',
    #     'comment': r'^\s*#\s*(.*)$',
    #     'key_value_pair': r'(.+)=(.+)',
    #     'empty': '^\n$',
    #     }
    # test = [
    #     '[section]',
    #     '  [section]   ',
    #     ' [ section  ] ',
    #     '    ',
    #     ]
    

    # for line, line_type in zip(rawlines, types):
    #     if line_type == 'comment':
    #         cfg.append([line_type])


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
