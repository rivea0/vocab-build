import csv
import pytest

import project

from rich.text import Text, Span

from style_screen import create_banner_panel, create_lower_panel_fields


def test_create_banner_panel():
    bp = create_banner_panel()
    assert bp.width == 50


def test_create_lower_panel_fields():
    fields = create_lower_panel_fields()
    assert fields == {
        'up_left': Text('-w, --word to add word to vocab-list.\n\nUsage: project.py -w [word]', no_wrap=False,
                       spans=[Span(0, 10, 'spring_green1 bold')]),
        'down_left': Text('-f, --file to add words from a csv file.\n\nUsage: project.py -f [file.csv]', no_wrap=False,
                         spans=[Span(0, 10, 'spring_green1 bold')]),
        'up_right': Text('-p, --play to play.\n\nUsage: project.py -p', no_wrap=False, spans=[Span(0, 10, 'spring_green1 bold')]),
        'down_right': Text(
            '-s, --sound to download pronunciation of the word.\n\nUsage: project.py -s [word]', no_wrap=False,
            spans=[Span(0, 11, 'spring_green1 bold')])
        }


# Fixtures for temporary csv files are adapted from:
# https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmpdir-factory-fixture

@pytest.fixture(scope='session')
def origin_csv_file(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('test-input-csv.csv')

    # Write test words and meanings to temporary input csv
    with open(fn, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['test_word', 'test_meaning'])
        writer.writerow(['another_test_word', 'another_test_meaning'])
    return fn


@pytest.fixture(scope='session')
def dest_csv_file(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('dest-csv.csv')

    # Write headers for the temporary destionation csv
    with open(fn, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['word', 'definition'])
        writer.writeheader()
    return fn


def test_add_word(dest_csv_file):
    project.add_word('hello', project.get_definition('hello'), dest_csv_file)
    assert project.word_already_in_list('hello', dest_csv_file) == True


def test_add_word_uppercase(dest_csv_file):
    project.add_word('UP', project.get_definition('UP'), dest_csv_file)
    assert project.word_already_in_list('up', dest_csv_file) == True


def test_add_words_from_file(origin_csv_file, dest_csv_file):
    project.add_words_from_file(origin_csv_file, dest_csv_file)

    # Assert that the words in origin_csv_file are added to the destination csv list
    assert project.get_definition_from_list('test_word', dest_csv_file) == 'test_meaning'
    assert project.get_definition_from_list('another_test_word', dest_csv_file) == 'another_test_meaning'


def test_word_already_in_list():
    assert project.word_already_in_list('juxtaposition', 'words.csv') == True
    assert project.word_already_in_list('abcde', 'words.csv') == False


def test_get_definition_from_list():
    assert project.get_definition_from_list('juxtaposition', 'words.csv') == 'the act of placing two things next to each other for implicit comparison'


def test_get_definition():
    assert project.get_definition('hello') == '"Hello!" or an equivalent greeting.'
    assert project.get_definition('dog') == 'A mammal, Canis familiaris or Canis lupus familiaris, that has been domesticated for thousands of years, of highly variable appearance due to human breeding.'


def test_get_audio_path():
    assert project.get_audio_path('hello') == 'https://api.dictionaryapi.dev/media/pronunciations/en/hello-au.mp3'


def test_get_all_words():
    with open('words.csv') as f:
        reader = csv.DictReader(f)
        all_words = {row['word']: row['definition'] for row in reader}
    assert len(all_words) == len(project.get_all_words())
