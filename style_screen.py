from time import sleep

from pyfiglet import Figlet

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.style import Style
from rich.text import Text


console = Console()
layout = Layout()


def create_welcome_figlet():
    """Create a welcome figlet for the opening screen."""
    f = Figlet(font='small')
    print(f.renderText('WELCOME TO VOCAB-BUILD!'))


def create_banner_panel():
    """Create the banner panel for the opening screen."""
    banner_panel_style = Style(color='white', frame=True, bold=True)
    banner_panel_text = Text('Choose an action below.',
                             justify='center',
                             style=banner_panel_style)
    banner_panel = Panel(banner_panel_text,
                         border_style='spring_green1',
                         width=50)
    return banner_panel


def organize_layout():
    """Organize the layout for the opening screen."""
    banner_panel = create_banner_panel()
    layout.split(
        Layout(Align(banner_panel, align='center', vertical='middle'),
               name='upper',
               minimum_size=2), Layout(name='lower', ratio=4))

    layout['lower'].split_row(Layout(name='left'), Layout(name='right'))


def create_lower_panel_fields():
    """Create four fields for the lower panel as hints of usage in the opening screen."""
    up_left_text = Text(
        '-w, --word to add word to vocab-list.\n\nUsage: project.py -w [word]',
        no_wrap=False)
    up_left_text.highlight_words(['-w, --word'], style='spring_green1 bold')

    down_left_text = Text(
        '-f, --file to add words from a csv file.\n\nUsage: project.py -f [file.csv]',
        no_wrap=False)
    down_left_text.highlight_words(['-f, --file'], style='spring_green1 bold')

    up_right_text = Text('-p, --play to play.\n\nUsage: project.py -p',
                         no_wrap=False)
    up_right_text.highlight_words(['-p, --play'], style='spring_green1 bold')

    down_right_text = Text(
        '-s, --sound to download pronunciation of the word.\n\nUsage: project.py -s [word]',
        no_wrap=False)
    down_right_text.highlight_words(['-s, --sound'],
                                    style='spring_green1 bold')

    return {
        'up_left': up_left_text,
        'down_left': down_left_text,
        'up_right': up_right_text,
        'down_right': down_right_text
    }


def split_lower_panel(fields):
    """Split the left and right fields of the lower panel."""
    layout['left'].split(
        Layout(Panel(fields['up_left'], border_style='white'), name='up_left'),
        Layout(Panel(fields['down_left'], border_style='white'),
               name='down_left'))

    layout['right'].split(
        Layout(Panel(fields['up_right'], border_style='white'),
               name='up_right'),
        Layout(Panel(fields['down_right'], border_style='white'),
               name='down_right'))


def display_opening_screen():
    """Display an opening screen when no argument is provided."""
    create_welcome_figlet()
    organize_layout()

    lower_panel_fields = create_lower_panel_fields()
    split_lower_panel(lower_panel_fields)

    sleep(1)
    console.print(layout)


def print_with_styling(message, style_to_apply='', end='\n\n'):
    """Print a message with a given styling and end character."""
    console.print(f'\n{message}', style=style_to_apply, end=end)
