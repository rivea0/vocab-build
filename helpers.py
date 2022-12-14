import random

from pathlib import Path
from time import sleep

from style_screen import print_with_styling


def create_sound_file(word, audio):
    """Create an mp3 file for the word pronunciation inside
    a sounds folder created in the current working directory.
    """
    # Create sounds folder if it doesn't exist
    sounds_folder = Path(f'{Path.cwd()}/sounds')
    if not sounds_folder.exists():
        sounds_folder.mkdir()
    mp3file_path = sounds_folder.joinpath(f'{word}.mp3')

    # Create mp3 file for the word if it doesn't exist
    if not mp3file_path.exists():
        with open(mp3file_path, 'wb') as f:
            f.write(audio.content)
            print_with_styling('Downloaded sound file successfully!', 'spring_green1')
    else:
        print_with_styling('Sound file already exists!', 'red')


def resolve_path(filename):
    """Return the absolute path of a given file."""
    if filename:
        try:
            p = Path(filename)
            return p.resolve(strict=True)
        except FileNotFoundError:
            raise


def get_random_definitions(words):
    """Get three random definitions from the given words dictionary."""
    return random.choices(list(words.values()), k=3)


def handle_correct_answer():
    """Print message that the answer is correct and wait 1 second."""
    print_with_styling('Correct!\n\nGet ready for the next word...', 'spring_green1')
    sleep(1)


def handle_wrong_answer(correct_answer):
    """Print message that the answer is wrong, display the correct answer, and wait 3 seconds."""
    print_with_styling('\nWrong answer!', 'red', end='\n')
    print_with_styling(f'The correct answer is: [spring_green1]{correct_answer}[/spring_green1]')
    print_with_styling('Get ready for the next word...')
    sleep(3)


def handle_invalid_number():
    """Print message that the answer is an invalid number, wait 1 second."""
    print_with_styling('Not a valid number!', 'red', end='\n')
    print_with_styling('Next question...')
    sleep(1)
