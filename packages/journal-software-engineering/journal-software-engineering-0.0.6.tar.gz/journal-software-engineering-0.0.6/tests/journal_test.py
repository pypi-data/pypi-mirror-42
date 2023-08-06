import os
import shutil
import pytest


@pytest.fixture(scope="module")
def journal_mock():
    from src import journal
    journal_path = os.path.join(
        os.path.expanduser(os.getcwd()),
        '.journal'
    )
    yield journal.Journal(journal_path)
    print("Removing created repo...")
    shutil.rmtree(journal_path)


def test_journal(journal_mock):
    journal_mock.journal_entry("journal")
    assert True


def test_journal_note(journal_mock):
    journal_mock.notes_entry("note")
    assert True


def test_journal_ticket(journal_mock):
    journal_mock.ticket_entry("ticket")
    assert True


def test_journal_todo(journal_mock):
    journal_mock.todo_entry("todo")
    assert True


def test_standup(journal_mock):
    journal_mock.standup(journal_mock.journal_repo, None, None)
    assert True
