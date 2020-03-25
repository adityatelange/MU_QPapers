import os
import logging

logger = logging.getLogger(__name__)
OWNER_ID = os.getenv("OWNER_ID")
# ----------------------------------------------------------------------------------------------------------------------
PM_START_TEXT = """Hello {}, my name is {}! If you have any questions on how to use me, read /help.
I'm a MU Student Assistant bot maintained by [this person](tg://user?id={}) ."""
# ----------------------------------------------------------------------------------------------------------------------

HELP_STRINGS = """*Main* commands available:
 - /start: start the bot
 - /help: send you this message.
And the following:
"""
HELPER_SCRIPTS = {}

# ----------------------------------------------------------------------------------------------------------------------
BASE_URL = "https://muquestionpapers.com/"
# ----------------------------------------------------------------------------------------------------------------------

COURSES_LIST = {'BE': 'be', 'ME': 'me', 'BSC': 'bs', "BCOM": 'bc', "BAF": 'ba', "BBI": 'bi', "BFM": 'bf', "BMS": 'bm', "MCA": 'mc'}
# ----------------------------------------------------------------------------------------------------------------------

BRANCHES_COURSE = {
    "BE": {'Automobile': 'am',
           'Biomedical': 'bm',
           'Biotechnology': 'bt',
           'Chemical': 'ch',
           'Civil': 'cl',
           'Computer': 'cp',
           'Electrical': 'el',
           'Electronics': 'et',
           'Electronics and Telecommunication': 'ex',
           'Information Technology': 'it',
           'Instrumentation': 'im',
           'Mechanical': 'mc',
           'Mechatronics': 'mt',
           'Production': 'pd',
           },
    "ME": {'CAD CAM and Robotics': 'cr',
           'Computer Engineering': 'cp',
           'CN & IS': 'ci',
           'Construction Engineering': 'cn',
           'Electronics Engineering': 'el',
           'Electronics & Telecommunication': 'ex',
           'Information Technology': 'it',
           'Machine Design': 'md',
           'Thermal Engineering': 'te',
           },
    "BSC": {'Biochemistry': 'bc',
            'Biotechnology': 'bt',
            'Botany': 'bo',
            'Chemistry': 'ch',
            'Computer Science (CS)': 'cs',
            'Information Technology': 'it',
            'Mathematics': 'mt',
            'Physics': 'ph',
            'Zoology': 'zo'
            },
    "BCOM": {'[default]': 'df'},
    "BAF": {'[default]': 'df'},
    "BBI": {'[default]': 'df'},
    "BFM": {'[default]': 'df'},
    "BMS": {'[default]': 'df'},
    "MCA": {'[default]': 'df'}
}
# ----------------------------------------------------------------------------------------------------------------------

SEMS = {
    'BE': ['1', '2', '3', '4', '5', '6', '7', '8'],
    'ME': ['1', '2'],
    'BSC': ['1', '2', '3', '4', '5', '6'],
    'BCOM': ['1', '2', '3', '4', '5', '6'],
    'BAF': ['1', '2', '3', '4', '5', '6'],
    'BBI': ['1', '2', '3', '4', '5', '6'],
    'BFM': ['1', '2', '3', '4', '5', '6'],
    'BMS': ['1', '2', '3', '4', '5', '6'],
    'MCA': ['1', '2', '3', '4', '5', '6']
}
# ----------------------------------------------------------------------------------------------------------------------
