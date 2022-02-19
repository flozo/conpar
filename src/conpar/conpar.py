#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main file of conpar."""

# Import modules
import argparse
import functions as fn
from colorama import init, Fore, Style
init()

# Define version string
version_num = '0.3'
version_dat = '2022-02-19'
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

    # Subparser read
    read_parser = subparsers.add_parser('read',
                                        aliases=['rea', 're', 'r', 'rd'],
                                        parents=[parent_parser],
                                        description='read config file',
                                        add_help=True)
    read_parser.add_argument('-c', '--comment',
                             default='#',
                             dest='comment_char',
                             help='define comment character (default: \'#\')')
    read_parser.add_argument('-s', '--section',
                             default='[]',
                             dest='section_marker',
                             help='define section marker(s): first character='
                             'opening marker, second character=closing marker '
                             '(default: \'[]\')')
    read_parser.add_argument('-a', '--assignment',
                             default='=',
                             dest='assignment_char',
                             help='define assignment character '
                             '(default: \'=\')')

    read_parser.add_argument('-r', '--raw', action='store_true',
                             help='show raw lines of config file')
    read_parser.add_argument('-p', '--parse', action='store_true',
                             help='show parsing result of config file on a '
                             'per-line basis')
    read_parser.add_argument('-d', '--dictionary', action='store_true',
                             help='show dictionary representation of '
                             'config file')
    read_parser.add_argument('-i', '--ini', action='store_true',
                             help='show ini representation of config file')
    read_parser.add_argument('-A', '--all', action='store_true',
                             help='combines optional arguments -rpd')

    # Subparser convert
    convert_parser = subparsers.add_parser('convert',
                                           aliases=['conver', 'conve', 'conv',
                                                    'con', 'co', 'c'],
                                           parents=[parent_parser],
                                           description='convert config file',
                                           add_help=True)
    convert_parser.add_argument('outfile', help='name of output file')

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
                     'key_value_sep': args.assignment_char,
                     }
    # Define colors for command-line output
    colors_dict = {'message': Fore.YELLOW,
                   'warning': Fore.RED,
                   'detail': Style.BRIGHT + Fore.MAGENTA,
                   'reset': Style.RESET_ALL,
                   }

    color = fn.Color(**colors_dict)

    print(color.detail + str(args))
    print(Style.RESET_ALL, end="")

    if (args.command in ('read', 'rea', 're', 'r', 'rd') or
            args.command in ('conver', 'conve', 'conv', 'con', 'co', 'c')):
        rawlines = fn.filetolist(args.infile)

    if args.command in ('read', 'rea', 're', 'r', 'rd'):
        print('{}[read] Reading file: \'{}\'{}'.format(color.message,
                                                       args.infile,
                                                       color.reset))
        # print(color.reset, end="")
        cfg = fn.Configuration(rawlines, **settings_dict)
        if args.all:
            print('{}[read] Optional argument \'--all\' = \'--raw '
                  '--parse --dictionary\'{}'.format(color.message,
                                                    color.reset))
        if args.raw or args.all:
            print('{}[read] Optional argument \'--raw\': Showing '
                  'raw lines of config file ...{}'.format(color.message,
                                                          color.reset))
            fn.printlist(rawlines)
        if args.parse or args.all:
            print('{}[read] Optional argument \'--parse\': Showing parsing '
                  'result of config file ...{}'.format(color.message,
                                                       color.reset))
            cfg_df = cfg.to_dataframe()
            print(cfg_df)
        if args.dictionary or args.all:
            print('{}[read] Optional argument \'--dictionary\': Showing '
                  'dictionary representation of config file '
                  '...{}'.format(color.message,
                                 color.reset))
            print('{}[warning] Comments and blank lines are not '
                  'supported!{}'.format(color.warning,
                                        color.reset))
            cfg_dict = cfg.to_dictionary()
            fn.printdict(cfg_dict)


if __name__ == '__main__':
    main()
