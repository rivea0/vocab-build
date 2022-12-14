import argparse
import csv
import random
import sys

import requests

import helpers

from style_screen import display_opening_screen, print_with_styling


# Add arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sound', help='download the pronunciation audio of the word')
parser.add_argument('-f', '--file', help='add words from a csv file')
parser.add_argument('-p', '--play', help='play vocabulary quiz', action='store_true')
parser.add_argument('-w', '--word', help='add word to the list')
args = parser.parse_args()


def main():
    # If there is no argument given, display the opening screen
    if sys.argv[0] == 'project.py' and len(sys.argv) == 1:
        display_opening_screen()
    elif len(sys.argv) == 3:
        opt_arg = sys.argv[1]
        if opt_arg in ('--word', '-w'):
            # Add the given word into the csv file if it does not exist,
            # display the word and its definition.
            if not word_already_in_list(args.word, 'words.csv'):
                try:
                    first_def = get_definition(args.word)
                except requests.HTTPError:
                    print_with_styling("Oops, an error occured. Couldn't get the word definition", 'red')
                    return
                except KeyError:
                    print_with_styling('Oops, no definitions found. Try another word.', 'red')
                    return

                add_word(args.word, first_def, 'words.csv')
                print_with_styling(f'[spring_green1]->[/spring_green1] {first_def}', 'bold', end='\n')
                print_with_styling('Word added to list!', 'spring_green1')
            else:
                d = get_definition_from_list(args.word, 'words.csv')
                print_with_styling(f'[spring_green1]->[/spring_green1] {d}', 'bold', end='\n')
                print_with_styling('Word already in list!', 'red')
        if opt_arg in ('--file', '-f'):
            # If the file given is a csv file, add the words into words.csv
            file_name = args.file
            if file_name.endswith('.csv'):
                try:
                    abs_path = helpers.resolve_path(args.file)
                    add_words_from_file(abs_path, 'words.csv')
                    print_with_styling('Words are added to file!', 'spring_green1')
                except FileNotFoundError:
                    print_with_styling('No such file exists!', 'red')
                    return
            else:
                print_with_styling('Not a csv file!', 'red')
                return
        if opt_arg in ('--sound', '-s'):
            # If the word has a valid audio path, create sounds folder and the mp3 file.
            word_to_sound = args.sound
            audio_path = get_audio_path(word_to_sound)
            if audio_path:
                audio = requests.get(audio_path)
                if audio.status_code == 200:
                    helpers.create_sound_file(word_to_sound, audio)
                else:
                    print_with_styling('Oops, something went wrong.', 'red')
            else:
                print_with_styling('Oops, no pronunciation audio is found.', 'red')

    elif len(sys.argv) == 2 and sys.argv[1] in ('-p', '--play'):
        print_with_styling('** Press CTRL+C to end the game. **', 'orange1')
        words = get_all_words()
        while True:
            try:
                # Get a random word, and its definition from all words
                word_to_ask = random.choice(list(words.keys()))
                def_of_word = words[word_to_ask]

                # Generate random definitions as potential answers (incorrect definitions for the word_to_ask)
                answer_candidates = helpers.get_random_definitions(words)

                # Add the correct definition to answer candidates
                answer_candidates.append(def_of_word)
            except IndexError:
                print_with_styling('No words in list!', 'red')

            try:
                print_with_styling(f'{word_to_ask}:', 'spring_green1 bold')
                random.shuffle(answer_candidates)

                # Display the definitions as well as their numbers
                for index, definition in enumerate(answer_candidates, start=1):
                    if definition == words[word_to_ask]:
                        correct_value = {index: definition}
                    print_with_styling(f'{index}. {definition}\n', end='')

                input_number = input('\nEnter the number of the correct definition: ')

                if not (1 <= int(input_number) <= 4):
                    helpers.handle_invalid_number()
                    continue
                if int(input_number) == list(correct_value.keys())[0]:
                    helpers.handle_correct_answer()
                else:
                    helpers.handle_wrong_answer(list(correct_value.values())[0])
            except (EOFError, KeyboardInterrupt):
                print_with_styling('\nGame ended.', 'orange1')
                break


def add_word(word, definition, filename):
    """Add a given word and its definition to the words.csv file."""
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([word.lower(), definition.lower()])


def add_words_from_file(path_to_input_file, dest_filename):
    """Add multiple words and definitions from a given csv file to the words.csv file."""
    with open(path_to_input_file) as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            if not word_already_in_list(row[0], dest_filename):
                add_word(row[0], row[1], dest_filename)


def word_already_in_list(word, filename):
    """Check if a given word is already in the words.csv file."""
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if word == row['word']:
                return True
    return False


def get_definition_from_list(word, filename):
    """Return the definition of a word from the words.csv file with styling."""
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if word == row['word']:
                return row['definition']


def get_definition(word):
    """Get the first definition of a given word."""
    endpoint = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    try:
        response = requests.get(endpoint).json()
        meanings = response[0]['meanings']
        return meanings[0]['definitions'][0]['definition']
    except KeyError:
        raise


def get_audio_path(word_to_sound):
    """Get the path to audio file of the pronunciation of a given word."""
    try:
        endpoint = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word_to_sound}'
        response = requests.get(endpoint).json()
        audio_path = response[0]['phonetics'][0]['audio']
        return audio_path
    except requests.HTTPError:
        print_with_styling("Oops, an error occured. Couldn't get the sound file.", 'red')
        return


def get_all_words():
    """Returns all the words and definitions from `words.csv` as a dictionary."""
    # Note to self: use it with caution.
    with open('words.csv') as f:
        reader = csv.DictReader(f)
        return {row['word']: row['definition'] for row in reader}



if __name__ == '__main__':
    main()
