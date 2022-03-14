#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main file of conpar."""

# Import modules
import argparse
import os
import functions as fn
import defaults as dflt


# Define version string
version_num = '0.14'
version_dat = '2022-03-14'
version_str = '{} ({})'.format(version_num, version_dat)


def main():
    """Define argument parsers and subparsers."""
    # Top-level parser
    parser = argparse.ArgumentParser(description='A parser for configuration '
                                     'files.')
    # Top-level-only options
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s '+version_str)

    # Subparser for subcommands
    subparsers = parser.add_subparsers(title='commands', dest='command',
                                       help='subcommands of fileops')

    # Parent parser
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Common options for all subparsers based on parent parser
    parent_parser.add_argument('infile', help='name of configuration file')
    parent_parser.add_argument('-v', '--verbose', action='count', default=0,
                               help='verbosity level (-v, -vv)')
    parent_parser.add_argument('-q', '--quiet', action='store_true',
                               help='disable terminal output (terminates all '
                               'verbosity)')
    parent_parser.add_argument('-D', '--dry-run', dest='dry',
                               action='store_true',
                               help='simulate execution of command')

    parent_parser.add_argument('-c', '--comment',
                               default='#',
                               dest='comment_char',
                               help='define comment character '
                               '(default: \'#\')')
    parent_parser.add_argument('-s', '--section',
                               default='[]',
                               dest='section_marker',
                               help='define section marker(s): first '
                               'character=opening marker, second '
                               'character=closing marker (default: \'[]\')')
    parent_parser.add_argument('-a', '--assignment',
                               default='=',
                               dest='assignment_char',
                               help='define assignment character '
                               '(default: \'=\')')

    # Subparser read
    read_parser = subparsers.add_parser('read',
                                        aliases=['rea', 're', 'r', 'rd'],
                                        parents=[parent_parser],
                                        description='read config file',
                                        add_help=True)

    read_parser.add_argument('-r', '--raw', action='store_true',
                             help='show raw lines of config file')
    read_parser.add_argument('-p', '--parse', action='store_true',
                             help='show parsing result of config file on a '
                             'per-line basis')
    read_parser.add_argument('-j', '--json', action='store_true',
                             help='show JSON representation of config file '
                             '(comments and blank lines are ignored)')
    read_parser.add_argument('-i', '--ini', action='store_true',
                             help='show INI representation of config file')
    read_parser.add_argument('-A', '--all', action='store_true',
                             help='combines optional arguments -rpj')

    # Subparser convert
    convert_parser = subparsers.add_parser('convert',
                                           aliases=['conver', 'conve', 'conv',
                                                    'con', 'co', 'c'],
                                           parents=[parent_parser],
                                           description='convert config file',
                                           add_help=True)
    convert_parser.add_argument('outfile', help='name of output file')
    convert_parser.add_argument('-j', '--json',
                                action='store_true',
                                help='convert to JSON file')
    convert_parser.add_argument('-i', '--ini',
                                action='store_true',
                                help='convert to INI file')

    args = parser.parse_args()

    # Check verbosity level
    verbosity = args.verbose
    if args.quiet is True:
        verbosity = -1
    if verbosity >= 1:
        print(args)

    # Define command aliases
    aliases_convert = ('convert', 'conver', 'conve', 'conv', 'con', 'co', 'c')
    aliases_read = ('read', 'rea', 're', 'r', 'rd')

    # Create config-settings object using specified arguments
    settings_dict = {'comment_char': args.comment_char,
                     'section_marker': args.section_marker,
                     'assignment_char': args.assignment_char,
                     }

    # Define colors for command-line output
    colors_dict = dflt.colors()

    # Create color object
    color = fn.Color(**colors_dict)

    # Handle undefined args.outfile
    if args.command in aliases_convert:
        outfile = args.outfile
    else:
        outfile = ''

    # Create configuration-file object
    config_file = fn.Config_file(args.infile)

    # Detect file extension
    extension = config_file.extension

    # Define command-line messages
    msg_dict = dflt.messages(color, args.infile, extension, outfile)

    # Create message object
    msg = fn.Message(**msg_dict)

    print(color.detail + str(args) + color.reset)

    if (args.command in aliases_read or args.command in aliases_convert):
        print(msg.read_file, end='')
        rawlines = config_file.to_list()
        print(msg.done)
        file_format = config_file.detect_format()

        if file_format == 'JSON':
            dict_json = fn.import_json(args.infile)
            cfg_json = fn.Configuration_JSON(dict_json)
            types = cfg_json.get_types()
            content = cfg_json.get_content()
            ini = fn.formatted(types, content, **settings_dict)
            cfg = fn.Configuration(types, content, list(dict_json), ini,
                                   **settings_dict)
        elif file_format == 'INI':
            cfg_ini = fn.Configuration_INI(rawlines, **settings_dict)
            types = cfg_ini.get_types()
            content = cfg_ini.get_content()
            json = list(cfg_ini.to_dictionary())
            ini = fn.formatted(types, content, **settings_dict)
            cfg = fn.Configuration(types, content, json, ini, **settings_dict)

    if args.command in aliases_read:
        if args.all:
            print(msg.arg_all)
        if args.raw or args.all:
            print(msg.arg_raw)
            fn.printlist(rawlines)
        if args.parse or args.all:
            print(msg.arg_parse)
            cfg_df = cfg.to_dataframe()
            print(cfg_df)
        if args.json or args.all:
            print(msg.arg_dict)
            print(msg.warn_comments)
            cfg_dict = cfg.to_dictionary()
            fn.printdict(cfg_dict)

    if args.command in aliases_convert:
        cfg = fn.Configuration_INI(rawlines, **settings_dict)
        if args.json:
            print(msg.arg_dict)
            print(msg.warn_comments)
            cfg_dict = cfg.to_dictionary()
            fn.printdict(cfg_dict)
            print(msg.write_file, end='')
            print(msg.done)
            fn.dict_to_json(args.outfile, cfg_dict)


if __name__ == '__main__':
    main()
