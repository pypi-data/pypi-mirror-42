import argparse
import os
import git
import re
from colorama import Fore, Style


class Journal:
    def __init__(self, journal_loc='~/.journal'):
        self.journal_path = os.path.expanduser(journal_loc)
        self.notes_path = os.path.join(self.journal_path, '.notes')
        self.todo_path = os.path.join(self.journal_path, '.todo')
        self.ticket_path = os.path.join(self.journal_path, '.ticket')
        if not os.path.exists(self.journal_path):
            os.makedirs(self.journal_path)
            r = git.Repo.init(self.journal_path)
            r.config_writer().set_value("user", "name", "journal").release()
            r.config_writer().set_value(
                "user", "email", "journal@gmail.com"
            ).release()
            readme_path = os.path.join(self.journal_path, 'README.md')
            open(readme_path, 'wb').close()
            r.index.add([readme_path])
            r.index.commit('initial commit')
        if not os.path.exists(self.notes_path):
            r = git.Repo.init(self.notes_path)
            r.config_writer().set_value("user", "name", "notes").release()
            r.config_writer().set_value(
                "user", "email", "notes@gmail.com"
            ).release()
            readme_path = os.path.join(self.notes_path, 'README.md')
            open(readme_path, 'wb').close()
            r.index.add([readme_path])
            r.index.commit('initial commit')
        if not os.path.exists(self.todo_path):
            r = git.Repo.init(self.todo_path)
            r.config_writer().set_value("user", "name", "todo").release()
            r.config_writer().set_value(
                "user", "email", "todo@gmail.com"
            ).release()
            readme_path = os.path.join(self.todo_path, 'README.md')
            open(readme_path, 'wb').close()
            r.index.add([readme_path])
            r.index.commit('initial commit')
        if not os.path.exists(self.ticket_path):
            r = git.Repo.init(self.ticket_path)
            r.config_writer().set_value("user", "name", "ticket").release()
            r.config_writer().set_value(
                "user", "email", "ticket@gmail.com"
            ).release()
            readme_path = os.path.join(self.ticket_path, 'README.md')
            open(readme_path, 'wb').close()
            r.index.add([readme_path])
            r.index.commit('initial commit')
        self.journal_repo = git.Repo(self.journal_path).git
        self.ticket_repo = git.Repo(self.ticket_path).git
        self.notes_repo = git.Repo(self.notes_path).git
        self.todo_repo = git.Repo(self.todo_path).git
        self.journal_name_map = {
            self.journal_repo: "JOURNAL",
            self.ticket_repo: "TICKET",
            self.notes_repo: "NOTES",
            self.todo_repo: "TODO"
        }

    def journal_entry(self, entry):
        self.journal_repo.commit(
            '--allow-empty', '-m', entry
        )

    def notes_entry(self, entry):
        self.journal_entry(entry)
        self.notes_repo.commit(
            '--allow-empty', '-m', entry
        )

    def ticket_entry(self, entry):
        self.journal_entry(entry)
        self.ticket_repo.commit(
            '--allow-empty', '-m', entry
        )

    def todo_entry(self, entry):
        self.journal_entry(entry)
        self.todo_repo.commit(
            '--allow-empty', '-m', entry
        )

    def standup(self, repo, before, after):
        print('\t{}{}{}{}'.format(
            Style.BRIGHT,
            Fore.MAGENTA,
            self.journal_name_map[repo],
            Style.RESET_ALL
        ))
        git_log_args = [
            '--pretty=format:"%s ~ %Cgreen[%cr]%Creset"',
            '--abbrev-commit'
        ]
        if before:
            git_log_args.append('--before="{}"'.format(before))
        if after:
            git_log_args.append('--since="{}"'.format(after))
        logs = repo.log(*git_log_args).split('\n')
        if logs == [u'']:
            print('{}{}{}'.format(
                Fore.RED,
                Style.BRIGHT,
                'No logs found for specified time frame',
                Fore.RESET,
                Style.RESET_ALL)
            )
            return
        for log in logs:
            m = re.search("(.*) ~ (.*)", log)
            message, time = m.groups()
            print('{}*{} {}{}{} - {}{}{}'.format(
                Fore.RED, Fore.RESET,
                Fore.YELLOW, time, Fore.RESET,
                Fore.GREEN, message, Fore.RESET
            ))
        print

    def main(self):
        parser = argparse.ArgumentParser(
            prog='journal',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='''
                journal makes commits to repos in the following locations:
                \tjournal location: {}
                \tnotes location: {}
                \tticket location: {}
                \ttodo location: {}'''.format(
                self.journal_path,
                self.notes_path,
                self.ticket_path,
                self.todo_path
            ),
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
            help='specifies to grab standup logs before entered date'
        )
        parser.add_argument(
            '-a', '--after', type=str,
            help='specifies to grab standup logs after entered date'
        )
        args = parser.parse_args()
        if args.standup:
            if args.ticket:
                self.standup(self.ticket_repo, args.before, args.after)
            if args.do:
                self.standup(self.todo_repo, args.before, args.after)
            if args.note:
                self.standup(self.notes_repo, args.before, args.after)
            if not args.ticket and not args.do and not args.note or args.journal:  # NOQA
                self.standup(self.journal_repo, args.before, args.after)
        else:
            if args.ticket:
                self.ticket_entry(args.entry)
            if args.do:
                self.todo_entry(args.entry)
            if args.note:
                self.notes_entry(args.entry)
            if not args.ticket and not args.do and not args.note or args.journal:  # NOQA
                self.journal_entry(args.entry)


if __name__ == '__main__':
    Journal().main()
