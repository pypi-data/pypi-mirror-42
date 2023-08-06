"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mjournal_software_engineering` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``journal_software_engineering.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``journal_software_engineering.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse

from journal import Journal
from journal import last_business_day

parser = argparse.ArgumentParser(
    prog='journal',
    description='''
    journal that provides functionality for generic,
    note, ticket, and todo journal entry and lookup
    functionality''',
    epilog='made by sage smith'
)

parser.add_argument(
    'entry', nargs='?', type=str,
    help='entry to enter in journal'
)
parser.add_argument(
    '-t', '--ticket', action='store_true',
    help='specifies ticket journal'
)
parser.add_argument(
    '-d', '--do', action='store_true',
    help='specifies todo journal'
)
parser.add_argument(
    '-n', '--note', action='store_true',
    help='specifies note journal'
)
parser.add_argument(
    '-c', '--complete', action='store_true',
    help='makes a completed entry in journal'
)
parser.add_argument(
    '-s', '--standup', action='store_true',
    help='prints stand up'
)
parser.add_argument(
    '-j', '--journal', action='store_true',
    help='specifies entire journal'
)
parser.add_argument(
    '-b', '--before', type=str,
    help='''
    specifies to grab standup logs before entered date
    format: YYYY-MM-DD
    '''
)
parser.add_argument(
    '-a', '--after', type=str,
    help='''
    specifies to grab standup logs after entered date
    default: last business day | format: YYYY-MM-DD
    ''',
    default=last_business_day()
)


def main(args=None):
    print('here')
    args = parser.parse_args()
    j = Journal()
    if args.standup:
        if args.ticket:
            j.standup(j.ticket_repo, args.before, args.after)
        if args.do:
            j.standup(j.todo_repo, args.before, args.after)
        if args.note:
            j.standup(j.notes_repo, args.before, args.after)
        if not args.ticket and not args.do and not args.note or args.journal:  # NOQA
            j.standup(j.journal_repo, args.before, args.after)
    else:
        if args.ticket:
            j.ticket_entry(args.entry)
        if args.do:
            j.todo_entry(args.entry)
        if args.note:
            j.notes_entry(args.entry)
        if not args.ticket and not args.do and not args.note or args.journal:  # NOQA
            j.journal_entry(args.entry)
    parser.print_help()
