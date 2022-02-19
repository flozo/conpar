#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of functions."""

import os
import pandas as pd
import json


class Color(object):
    """Define colors for command-line output."""

    def __init__(self, message, warning, detail, reset):
        self.message = message
        self.warning = warning
        self.detail = detail
        self.reset = reset


class Config_settings:
    """Define configuration settings."""

    def __init__(self, comment_char='#', section_marker='[]',
                 key_value_sep='='):
        self.comment_char = comment_char
        self.section_marker = section_marker
        self.key_value_sep = key_value_sep


class Line(Config_settings):
    """Define single-line properties and methods."""

    def __init__(self, rawline, comment_char, section_marker, key_value_sep):
        super().__init__(comment_char, section_marker, key_value_sep)
        self.rawline = rawline
        # Create a version of rawline without leading and trailing spaces
        self.line = self.rawline.strip()

    # Functions for determining content type

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
        if (len(self.section_marker) == 2 and
                self.line[-1] == self.section_marker[1]):
            return True
        else:
            return False

    def is_unknown(self):
        """Check if line type is unknown."""
        if not(self.is_comment() or self.is_empty() or
               self.is_key_value_pair() or self.is_section()):
            return True
        else:
            return False

    # Functions for extracting content

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


class Configuration(Config_settings):
    """Define configuration properties and methods."""

    def __init__(self, rawlines, comment_char, section_marker, key_value_sep):
        super().__init__(comment_char, section_marker, key_value_sep)
        self.rawlines = rawlines

    def get_types(self):
        """Determine configuration content type."""
        types = []
        for rawline in self.rawlines:
            line = Line(rawline, self.comment_char, self.section_marker,
                        self.key_value_sep)
            if line.is_comment() is True:
                types.append('comment')
            elif line.is_empty() is True:
                types.append('empty')
            elif line.is_section() is True:
                types.append('section_head')
            elif line.is_key_value_pair() is True:
                types.append('key_value_pair')
            else:
                types.append('unknown')
        return types

    def get_content(self):
        """Determine line contents."""
        content = []
        for rawline in self.rawlines:
            line = Line(rawline, self.comment_char, self.section_marker,
                        self.key_value_sep)
            if line.is_comment() is True:
                content.append(line.comment())
            elif line.is_empty() is True:
                content.append('')
            elif line.is_section() is True:
                content.append(line.section_name())
            elif line.is_key_value_pair() is True:
                content.append(line.key_value_pair())
            else:
                content.append(line.rawline)
        return content

    def formatted(self):
        """Create nicely formatted config-file lines."""
        clean_lines = []
        for line_type, content in zip(self.get_types(), self.get_content()):
            if line_type == 'comment':
                clean_lines.append('{} {}'.format(self.comment_char, content))
            elif line_type == 'empty':
                clean_lines.append('')
            elif line_type == 'section_head':
                sec_line = '{} {}'.format(self.section_marker[0], content)
                if len(self.section_marker) == 2:
                    sec_line = sec_line + ' ' + self.section_marker[1]
                clean_lines.append(sec_line)
            elif line_type == 'key_value_pair':
                clean_lines.append('{} {} {}'.format(content[0],
                                                     self.key_value_sep,
                                                     content[1]))
            else:
                clean_lines.append(content)
        return clean_lines

    def to_dataframe(self):
        """Create Pandas DataFrame with all information."""
        cfg_dict = {
            'TYPE': self.get_types(),
            'CONTENT': self.get_content(),
            'RAW': self.rawlines,
            'FORMATTED': self.formatted(),
            }
        df = pd.DataFrame(cfg_dict)
        # Label unnamed auto-index
        df.index.name = 'LINE'
        return df

    def to_dictionary(self):
        """Create dictionary with sections and key-value pairs."""
        # Get series of section heads
        section_heads = self.to_dataframe()['CONTENT'][self.to_dataframe()['TYPE'] == 'section_head']
        # Get series of key-value pairs
        key_value_pairs = self.to_dataframe()['CONTENT'][self.to_dataframe()['TYPE'] == 'key_value_pair']
        # Initialize section list
        section = []
        for i, section_head in enumerate(section_heads):
            # Determine start index for i-th section head
            start = section_heads.index.values[i]
            if i < len(section_heads)-1:
                # Determine stop index for i-th section head
                stop = section_heads.index.values[i+1]
            else:
                # Determine stop index for final section head
                stop = key_value_pairs.index[-1]
            # Cast key-value pairs between start and stop into list, then dict
            section.append(dict(list(key_value_pairs.loc[start:stop])))
        # Return dictionary with section heads as first-level keys and
        # sub-dictionaries with key-value pairs as values
        return dict(zip(section_heads, section))

    def export_json(self, filename):
        """Export config data to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.to_dictionary(), f, indent=4)

    def import_json(self, filename):
        """Read JSON file and write content into nested dictionary."""
        with open(filename, 'r') as f:
            config_dict = json.load(f)
        return config_dict

    def from_dictionary(self, json_dict):
        """Convert JSON dict to labeled dict."""
        # df = pd.DataFrame.from_dict(json_dict)
        sections = list(json_dict.keys())
        keys = list(list(json_dict.values())[0].keys())
        values = list(list(json_dict.values())[0].values())
        key_value_pairs = list(zip(keys, values))
        list1 = []
        for i, section in enumerate(sections):
            keys = list(list(json_dict.values())[i].keys())
            values = list(list(json_dict.values())[i].values())
            key_value_pairs = list(zip(keys, values))
            list1.append(section)
            for pair in key_value_pairs:
                list1.append(pair)
        return list1


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


def printlist(rawlines):
    """Print all lines."""
    for line in rawlines:
        print(line)


def printdict(dictionary):
    """Pretty-print dictionary."""
    print(json.dumps(dictionary, sort_keys=True, indent=4))


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
