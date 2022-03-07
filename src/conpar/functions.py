#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of functions."""

import os
import pandas as pd
import json
import defaults as dflt


class Color(object):
    """Define colors for command-line output."""

    def __init__(self, message, warning, success, detail, reset):
        self.message = message
        self.warning = warning
        self.success = success
        self.detail = detail
        self.reset = reset


class Message(object):
    """Define messages for command-line output."""

    def __init__(self, arg_all, arg_raw, arg_parse, arg_dict, arg_ini,
                 read_file, write_file, extension, other_extension, test_json,
                 test_ini, is_json, is_ini, unknown, done, success, failure,
                 warn_comments):
        self.arg_all = arg_all
        self.arg_raw = arg_raw
        self.arg_parse = arg_parse
        self.arg_dict = arg_dict
        self.arg_ini = arg_ini
        self.read_file = read_file
        self.write_file = write_file
        self.extension = extension
        self.other_extension = other_extension
        self.test_json = test_json
        self.test_ini = test_ini
        self.is_json = is_json
        self.is_ini = is_ini
        self.unknown = unknown
        self.done = done
        self.success = success
        self.failure = failure
        self.warn_comments = warn_comments


class Config_file(object):
    """Define configuration-file properties and methods."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.directory = os.path.dirname(file_path)
        self.filename = os.path.basename(file_path)
        self.extension = os.path.splitext(file_path)[-1]
        self.format = self.detect_format()

    def to_list(self):
        """Read file into list line by line."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = []
            for line in f:
                lines.append(line.rstrip())
        return lines

    def is_json(self):
        """Check if file is JSON."""
        try:
            with open(self.file_path, 'r') as f:
                json.load(f)
        except ValueError:
            return False
        return True

    def is_ini(self):
        """Check if file is INI."""
        rawlines = self.to_list()
        assignment_char = '='
        for line in rawlines:
            # Check if assignment character is present
            if assignment_char in line:
                # Check if assignment character is surrounded by key-value pair
                if line.split('=')[0] != '' and line.split('=')[1] != '':
                    return True
        return False

    def detect_format(self):
        """Detect configuration-file format (JSON or INI)."""
        colors_dict = dflt.colors()
        color = Color(**colors_dict)
        msg_dict = dflt.messages(color, self.file_path, self.extension, '')
        msg = Message(**msg_dict)
        file_format = 'unknown'
        # Use filename extension as hint for file format
        if self.extension in ('.json', '.ini'):
            print(msg.extension)
        else:
            print(msg.other_extension)
        if self.extension != '.ini':
            print(msg.test_json, end='')
            is_json = self.is_json()
            if is_json is True:
                file_format = 'JSON'
                print(msg.success)
                print(msg.is_json)
            else:
                print(msg.failure)
                print(msg.test_ini, end='')
                is_ini = self.is_ini()
                if is_ini is True:
                    file_format = 'INI'
                    print(msg.success)
                    print(msg.is_ini)
                else:
                    print(msg.failure)
                    print(msg.unknown)
        elif self.extension == '.ini':
            print(msg.test_ini, end='')
            is_ini = self.is_ini()
            if is_ini is True:
                file_format = 'INI'
                print(msg.success)
                print(msg.is_ini)
            else:
                print(msg.failure)
                print(msg.test_json, end='')
                is_json = self.is_json()
                if is_json is True:
                    file_format = 'JSON'
                    print(msg.success)
                    print(msg.is_json)
                else:
                    print(msg.failure)
                    print(msg.unknown)
        return file_format


class Config_settings(object):
    """Define configuration settings."""

    def __init__(self, comment_char='#', section_marker='[]',
                 assignment_char='='):
        self.comment_char = comment_char
        self.section_marker = section_marker
        self.assignment_char = assignment_char


class Line_INI(Config_settings):
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


class Configuration_INI(Config_settings):
    """Define INI configuration properties and methods."""

    def __init__(self, rawlines, comment_char, section_marker,
                 assignment_char):
        super().__init__(comment_char, section_marker, assignment_char)
        self.rawlines = rawlines

    def get_types(self):
        """Determine configuration content type."""
        types = []
        for rawline in self.rawlines:
            line = Line_INI(rawline, self.comment_char, self.section_marker,
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
            line = Line_INI(rawline, self.comment_char, self.section_marker,
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
            'FORMATTED': formatted(self.get_types(), self.get_content(),
                                   self.comment_char, self.section_marker,
                                   self.assignment_char),
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


class Configuration_JSON(object):
    """Define INI configuration properties and methods."""

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def get_content(self):
        """Convert JSON dict to list."""
        # df = pd.DataFrame.from_dict(json_dict)
        sections = list(self.dictionary.keys())
        keys = list(list(self.dictionary.values())[0].keys())
        values = list(list(self.dictionary.values())[0].values())
        key_value_pairs = list(zip(keys, values))
        list1 = []
        for i, section in enumerate(sections):
            keys = list(list(self.dictionary.values())[i].keys())
            values = list(list(self.dictionary.values())[i].values())
            key_value_pairs = list(zip(keys, values))
            list1.append(section)
            for pair in key_value_pairs:
                list1.append(pair)
        return list1

    def get_types(self):
        """Determine content type."""
        types = []
        for line in self.get_content():
            if type(line) is tuple:
                types.append('key_value_pair')
            else:
                types.append('section_head')
        return types


class Configuration(Config_settings):
    """Define generic configuration object."""

    def __init__(self, types, content, json, ini, comment_char, section_marker,
                 assignment_char):
        super().__init__(comment_char, section_marker, assignment_char)
        self.types = types
        self.content = content
        self.json = json
        self.ini = ini

    def to_dataframe(self):
        """Create Pandas DataFrame with all information."""
        cfg_dict = {
            'TYPE': self.types,
            'CONTENT': self.content,
            'JSON': self.json,
            'INI': self.ini,
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


def import_json(filename):
    """Read JSON file and write content into nested dictionary."""
    with open(filename, 'r') as f:
        config_dict = json.load(f)
    return config_dict


# def from_dictionary(json_dict):
#     """Convert JSON dict to labeled dict."""
#     # df = pd.DataFrame.from_dict(json_dict)
#     sections = list(json_dict.keys())
#     keys = list(list(json_dict.values())[0].keys())
#     values = list(list(json_dict.values())[0].values())
#     key_value_pairs = list(zip(keys, values))
#     list1 = []
#     for i, section in enumerate(sections):
#         keys = list(list(json_dict.values())[i].keys())
#         values = list(list(json_dict.values())[i].values())
#         key_value_pairs = list(zip(keys, values))
#         list1.append(section)
#         for pair in key_value_pairs:
#             list1.append(pair)
#     return list1


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


# def ini_to_dataframe(lines_list, comment_char, section_marker, assignment_char):
#     types = list_get_types(lines_list)
#     cfg_dict = {
#         'TYPE': types,
#         'CONTENT': lines_list,
#         'INI_FORMATTED': formatted(types, lines_list, comment_char, section_marker, assignment_char)
#         }
#     df = pd.DataFrame(cfg_dict)
#     # Label unnamed auto-index
#     df.index.name = 'LINE'
#     return df


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


def is_ini_str(string, comment_char, section_marker, assignment_char):
    """Check if string is INI."""
    # Create line object
    cfg = Line_INI(string, comment_char, section_marker, assignment_char)
    # Return opposite of is_unknown() boolean
    return not(cfg.is_unknown())


# def parse_config_verbose(infile, extension, settings_dict, msg):
#     file_format = 'unknown'
#     if extension in ('.json', '.ini'):
#         print(msg.extension)
#     else:
#         print(msg.other_extension)
#     if extension != '.ini':
#         print(msg.test_json, end='')
#         is_json = is_json_file(infile)
#         if is_json is True:
#             file_format = 'JSON'
#             print(msg.success)
#             print(msg.is_json)
#         else:
#             print(msg.failure)
#             print(msg.test_ini, end='')
#             is_ini = is_ini_file(infile, **settings_dict)
#             if is_ini is True:
#                 file_format = 'INI'
#                 print(msg.success)
#                 print(msg.is_ini)
#             else:
#                 print(msg.failure)
#                 print(msg.unknown)
#     elif extension == '.ini':
#         print(msg.test_ini, end='')
#         is_ini = is_ini_file(infile, **settings_dict)
#         if is_ini is True:
#             file_format = 'INI'
#             print(msg.success)
#             print(msg.is_ini)
#         else:
#             print(msg.failure)
#             print(msg.test_json, end='')
#             is_json = is_json_file(infile)
#             if is_json is True:
#                 file_format = 'JSON'
#                 print(msg.success)
#                 print(msg.is_json)
#             else:
#                 print(msg.failure)
#                 print(msg.unknown)
#     return file_format


# def parse_config_quiet(infile, extension, settings_dict):
#     file_format = 'unknown'
#     if extension != '.ini':
#         is_json = is_json_file(infile)
#         if is_json is True:
#             file_format = 'JSON'
#         else:
#             is_ini = is_ini_file(infile, **settings_dict)
#             if is_ini is True:
#                 file_format = 'INI'
#     elif extension == '.ini':
#         is_ini = is_ini_file(infile, **settings_dict)
#         if is_ini is True:
#             file_format = 'INI'
#         else:
#             is_json = is_json_file(infile)
#             if is_json is True:
#                 file_format = 'JSON'
#     return file_format


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
