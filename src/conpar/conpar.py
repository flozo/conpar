#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main file of conpar."""

# Import modules
import argparse
# import os
import functions as fn
# import pandas as pd
# import json
# import datetime
# import uuid


# Define version string
version_num = '0.2'
version_dat = '2022-02-09'
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
    parent_parser.add_argument('filename', help='name of configuration file')
    parent_parser.add_argument('-v', '--verbose', action='count', default=0,
                               help='verbosity level (-v, -vv, -vvv)')
    parent_parser.add_argument('-q', '--quiet', action='store_true',
                               help='disable terminal output (terminates all verbosity)')
    parent_parser.add_argument('-D', '--dry-run', dest='dry',
                               action='store_true',
                               help='simulate execution of command')

    # Subparser settings
    settings_parser = subparsers.add_parser('settings',
                                         aliases=['setting', 'settin', 'setti',
                                                  'sett', 'set', 'se', 's'],
                                         parents=[parent_parser],
                                         description='edit settings',
                                         add_help=True)
    settings_parser.add_argument('-s', '--show', action='store_true',
                                           help='show settings')
    settings_parser.add_argument('-o', '--open',
                                           help='open settings file with '
                                           'default editor')

    # Subparser create
    create_parser = subparsers.add_parser('create',
                                         aliases=['creat', 'crea', 'cre',
                                                  'cr', 'c'],
                                         parents=[parent_parser],
                                         description='create table',
                                         add_help=True)
    create_parser.add_argument('table_name', help='table name')
    create_parser.add_argument('column_name', nargs='*', help='column name')

    args = parser.parse_args()

    # Check verbosity level
    verbosity = args.verbose
    if args.quiet is True:
        verbosity = -1
    if verbosity >= 1:
        print(args)

    print(args)

    # # Use settings directory or create one
    # settings_dir = os.path.expanduser('~/.config/conpar')
    # fn.check_config_dir(settings_dir)
    # # Use settings file or create one
    # settings_file = os.path.join(settings_dir, 'settings.ini')
    # fn.check_config_file(settings_file)


# text = fn.read_text(os.path.join(config_dir, 'letter.txt'))
# text = fn.format_text(text)

    # if args.command in ('settings', 'setting', 'settin', 'setti', 'sett',
    #                     'set', 'se', 's'):
    #     if args.show:
    #         print(fn.read_config(settings_file).get())
    #     else:
    #         os.system('xdg-open {}'.format(settings_file))

    # directory = 'Dokumente/Finanzen/Daten'
    # data_dir = os.path.expanduser('~/{}'.format(directory))
    # if args.dry:
    #     print('[dry run] Nothing fetched.')


if __name__ == '__main__':
    main()
