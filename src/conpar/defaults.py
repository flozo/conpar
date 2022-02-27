#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of default values."""

from colorama import init, Fore, Style
init()


def colors():
    """Define colors for command-line output."""
    colors_dict = {'message': Fore.YELLOW,
                   'warning': Fore.RED,
                   'success': Fore.GREEN,
                   'detail': Style.BRIGHT + Fore.MAGENTA,
                   'reset': Style.RESET_ALL,
                   }
    return colors_dict


def messages(color, infile, extension, outfile):
    """Define command-line messages."""
    msg_dict = {
        'arg_all': '{}[read] Optional argument \'--all\' = \'--raw '
                   '--parse --json\'{}'.format(color.message,
                                               color.reset),
        'arg_raw': '{}[read] Optional argument \'--raw\': Showing '
                   'raw lines of config file ...{}'.format(color.message,
                                                           color.reset),
        'arg_parse': '{}[read] Optional argument \'--parse\': Showing '
                     'parsing result of config file '
                     '...{}'.format(color.message, color.reset),
        'arg_dict': '{}[read] Optional argument \'--json\': Showing '
                    'JSON representation of config file '
                    '...{}'.format(color.message,
                                   color.reset),
        'arg_ini': 'Bla',
        'read_file': '{}[read] Reading file: '
        '\'{}\' ...{}'.format(color.message,
                              infile,
                              color.reset),
        'write_file': '{}[convert] Writing file: '
                      '\'{}\' ...{}'.format(color.message,
                                            outfile,
                                            color.reset),
        'extension': '{}[read] File-name extension \'{}\' suggests {} '
                     'format.{}'.format(color.message,
                                        extension,
                                        extension[1:].upper(),
                                        color.reset),
        'other_extension': '{}[warning] Unexpected file-name extension \'{}\' '
                           '(expected \'.json\' or '
                           '\'.ini\').{}'.format(color.warning,
                                                 extension,
                                                 color.reset),
        'test_json': '{}[read] Try parsing JSON format '
                     '...{}'.format(color.message,
                                    color.reset),
        'test_ini': '{}[read] Try parsing INI format '
                    '...{}'.format(color.message,
                                   color.reset),
        'is_json': '{}[read] Detected JSON format.{}'.format(color.message,
                                                             color.reset),
        'is_ini': '{}[read] Detected INI format.{}'.format(color.message,
                                                           color.reset),
        'unknown': '{}[error] Unknown file format!{}'.format(color.warning,
                                                             color.reset),
        'done': '{} DONE!{}'.format(color.message,
                                    color.reset),
        'success': '{} SUCCESS!{}'.format(color.success,
                                          color.reset),
        'failure': '{} FAILURE!{}'.format(color.warning,
                                          color.reset),
        'warn_comments': '{}[warning] Conversion to JSON does not conserve '
                         'comments and blank lines!{}'.format(color.warning,
                                                              color.reset),
        }
    return msg_dict
