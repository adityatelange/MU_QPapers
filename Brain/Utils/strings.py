import os
import logging

logger = logging.getLogger(__name__)
OWNER_ID = os.getenv("OWNER_ID")
# ----------------------------------------------------------------------------------------------------------------------
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
    'BE': 8,
    'ME': 2,
    'BSC': 6,
    'BCOM': 6,
    'BAF': 6,
    'BBI': 6,
    'BFM': 6,
    'BMS': 6,
    'MCA': 6
}
# ----------------------------------------------------------------------------------------------------------------------
