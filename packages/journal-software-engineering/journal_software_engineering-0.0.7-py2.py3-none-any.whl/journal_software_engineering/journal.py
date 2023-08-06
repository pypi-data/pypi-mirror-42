import os
import re

import git
from colorama import Fore
from colorama import Style


def last_business_day():
    import pandas as pd
    # BDay is business day, not birthday...
    from pandas.tseries.offsets import BDay

    # pd.datetime is an alias for datetime.datetime
    today = pd.datetime.today()
    return (today - BDay(1)).strftime("%Y-%m-%d")


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
