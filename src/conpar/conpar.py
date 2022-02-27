#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main file of conpar."""

# Import modules
import argparse
import os
import functions as fn
import defaults as dflt


# Define version string
version_num = '0.8'
version_dat = '2022-02-27'
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
    if args.command in ('convert', 'conver', 'conve', 'conv', 'con', 'co',
                        'c'):
        outfile = args.outfile
    else:
        outfile = ''

    # Detect file extension
    extension = os.path.splitext(args.infile)[-1]

    # Define command-line messages
    msg_dict = dflt.messages(color, args.infile, extension, outfile)

    # Create message object
    msg = fn.Message(**msg_dict)

    print(color.detail + str(args) + color.reset)

    if (args.command in ('read', 'rea', 're', 'r', 'rd') or
            args.command in ('convert', 'conver', 'conve', 'conv', 'con', 'co',
                             'c')):
        print(msg.read_file, end='')
        rawlines = fn.filetolist(args.infile)
        print(msg.done)
        if extension in ('.json', '.ini'):
            print(msg.extension)
        else:
            print(msg.other_extension)
        if extension != '.ini':
            print(msg.test_json, end='')
            is_json = fn.is_json_file(args.infile)
            if is_json is True:
                print(msg.success)
                print(msg.is_json)
            else:
                print(msg.failure)
                print(msg.test_ini, end='')
                is_ini = fn.is_ini_file(args.infile, **settings_dict)
                if is_ini is True:
                    print(msg.success)
                    print(msg.is_ini)
                else:
                    print(msg.failure)
                    print(msg.unknown)
        elif extension == '.ini':
            print(msg.test_ini, end='')
            is_ini = fn.is_ini_file(args.infile, **settings_dict)
            if is_ini is True:
                print(msg.success)
                print(msg.is_ini)
            else:
                print(msg.failure)
                print(msg.test_json, end='')
                is_json = fn.is_json_file(args.infile)
                if is_json is True:
                    print(msg.success)
                    print(msg.is_json)
                else:
                    print(msg.failure)
                    print(msg.unknown)
        # print(msg.done)

    if args.command in ('read', 'rea', 're', 'r', 'rd'):
        cfg = fn.Configuration(rawlines, **settings_dict)
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

    if args.command in ('convert', 'conver', 'conve', 'conv', 'con', 'co',
                        'c'):
        cfg = fn.Configuration(rawlines, **settings_dict)
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
