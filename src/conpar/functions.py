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


class Message(object):
    """Define messages for command-line output."""

    def __init__(self, arg_all, arg_raw, arg_parse, arg_dict, arg_ini,
                 read_file, write_file, done, warn_comments):
        self.arg_all = arg_all
        self.arg_raw = arg_raw
        self.arg_parse = arg_parse
        self.arg_dict = arg_dict
        self.arg_ini = arg_ini
        self.read_file = read_file
        self.write_file = write_file
        self.done = done
        self.warn_comments = warn_comments


class Config_settings(object):
    """Define configuration settings."""

    def __init__(self, comment_char='#', section_marker='[]',
                 assignment_char='='):
        self.comment_char = comment_char
        self.section_marker = section_marker
        self.assignment_char = assignment_char


class Line(Config_settings):
    """Define single-line properties and methods."""

    def __init__(self, rawline, comment_char, section_marker, assignment_char):
        super().__init__(comment_char, section_marker, assignment_char)
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
        if self.assignment_char in self.line:
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
            return (self.line.split(self.assignment_char)[0].strip(),
                    self.line.split(self.assignment_char)[1].strip())

    def section_name(self):
        """If line is section head, return section name."""
        # Check if line is a section head
        if self.is_section() is True:
            # Return section name without leading and trailing spaces
            return self.line[1:-1].strip()


class Configuration(Config_settings):
    """Define configuration properties and methods."""

    def __init__(self, rawlines, comment_char, section_marker,
                 assignment_char):
        super().__init__(comment_char, section_marker, assignment_char)
        self.rawlines = rawlines

    def get_types(self):
        """Determine configuration content type."""
        types = []
        for rawline in self.rawlines:
            line = Line(rawline, self.comment_char, self.section_marker,
                        self.assignment_char)
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
                        self.assignment_char)
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

    def count_types(self):
        """Return dict with frequencies of config-file line types."""
        type_count = self.to_dataframe()['TYPE'].value_counts()
        types = [
            'comment',
            'empty',
            'section_head',
            'key_value_pair',
            'unknown'
            ]
        return dict(type_count.reindex(types, fill_value=0))
        # .rename_axis('TYPE').reset_index(name='COUNTS')

    def to_dictionary(self):
        """Create dictionary with sections and key-value pairs."""
        df = self.to_dataframe()
        # Get series of section heads
        section_heads = df['CONTENT'][df['TYPE'] == 'section_head']
        # Get series of key-value pairs
        key_value_pairs = df['CONTENT'][df['TYPE'] == 'key_value_pair']
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


def formatted(types, content, comment_char, section_marker, assignment_char):
    """Create nicely formatted config-file lines."""
    clean_lines = []
    for line_type, content in zip(types, content):
        if line_type == 'comment':
            clean_lines.append('{} {}'.format(comment_char, content))
        elif line_type == 'empty':
            clean_lines.append('')
        elif line_type == 'section_head':
            sec_line = '{} {}'.format(section_marker[0], content)
            if len(section_marker) == 2:
                sec_line = sec_line + ' ' + section_marker[1]
            clean_lines.append(sec_line)
        elif line_type == 'key_value_pair':
            clean_lines.append('{} {} {}'.format(content[0],
                                                 assignment_char,
                                                 content[1]))
        else:
            clean_lines.append(content)
    return clean_lines


def list_get_types(lines_list):
    types = []
    for line in lines_list:
        if type(line) is tuple:
            types.append('key_value_pair')
        else:
            types.append('section_head')
    return types


def ini_to_dataframe(lines_list, comment_char, section_marker, assignment_char):
    types = list_get_types(lines_list)
    cfg_dict = {
        'TYPE': types,
        'CONTENT': lines_list,
        'FORMATTED': formatted(types, lines_list, comment_char, section_marker, assignment_char)
        }
    df = pd.DataFrame(cfg_dict)
    # Label unnamed auto-index
    df.index.name = 'LINE'
    return df


def dataframe_to_ini_list(df):
    types = list(df['TYPE'])
    contents = list(df['FORMATTED'])
    ini_list = []
    for i, line in enumerate(types):
        # Insert blank line before new section, except first one
        if line == 'section_head' and i > 0:
            ini_list.append('')
        ini_list.append(contents[i])
    return ini_list


def filetolist(infile):
    """
    Read file into list line by line.

    Parameters
    ----------
    infile : string
        name of input file.

    Returns
    -------
    lines : list of strings
        list of file rows.
    """
    with open(infile, 'r', encoding='utf-8') as f:
        lines = []
        for line in f:
            lines.append(line.rstrip())
    return lines


def listtofile(outfile, lines):
    """
    Write list to file.

    Parameters
    ----------
    outfile : string
        filename for output.
    listname : list of strings
        list to be written to file.

    Returns
    -------
    None.
    """
    with open(outfile, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def dict_to_json(outfile, settings_dict):
    """Write config file."""
    with open(outfile, 'w') as f:
        json.dump(settings_dict, f, indent=4)


def printlist(rawlines):
    """Print all lines."""
    for line in rawlines:
        print(line)


def printdict(dictionary):
    """Pretty-print dictionary."""
    print(json.dumps(dictionary, sort_keys=False, indent=4))


def is_json_str(string):
    """Check if string is JSON."""
    try:
        json.loads(string)
    except ValueError:
        return False
    return True


def is_json_file(infile):
    """Check if file is JSON."""
    try:
        with open(infile, 'r') as f:
            json.load(f)
    except ValueError:
        return False
    return True


def is_ini_str(string, comment_char, section_marker, assignment_char):
    """Check if string is INI."""
    # Create line object
    cfg = Line(string, comment_char, section_marker, assignment_char)
    # Return opposite of is_unknown() boolean
    return not(cfg.is_unknown())


def is_ini_file(infile, comment_char, section_marker, assignment_char):
    """Check if string is INI."""
    rawlines = filetolist(infile)
    cfg = Configuration(rawlines, comment_char, section_marker,
                        assignment_char)
    # At least one key-value pair is needed:
    print(cfg.count_types()['key_value_pair'])
    if cfg.count_types()['key_value_pair'] > 0:
        return True
    else:
        return False


# def check_config_dir(config_dir):
#     """Check if config directory exists. If not, ask for creating one."""
#     if not os.path.isdir(config_dir):
#         print('[config] Config directory {} not found.'.format(config_dir))
#         create_config_dir = input('[config] Create config directory {} ? '
#                                   '(Y/n): '.format(config_dir))
#         if create_config_dir == 'Y':
#             os.makedirs(config_dir)
#             print('[config] Config directory {} created.'.format(config_dir))
#         else:
#             print('[config] No config directory created.')
