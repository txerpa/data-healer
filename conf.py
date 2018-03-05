# -*- coding: utf-8 -*-

"""
Application configuration file
In this file the user must specify some options for the automatization of the categorization task
"""

import os

ROOT_DIR = os.path.abspath(__file__).split('conf.py')[0]


# ======================================================================================================================
# Input configuration
# ======================================================================================================================

# Input dataset file
INPUT_FILE = ROOT_DIR + 'data/N12022_D2018-02-26_preprocessed.csv'

# Input CSV file row separator
INPUT_SEPARATOR = ';'

# Columns to show in the screen (information that the user needs to categorize the row)
COLUMNS_TO_SHOW = ['original_messages', ]

# If this column is not None the category of this column will be used as a clue for the user
# (this column could have been inferred by an unsupervised learning algorithm)
HELP_COLUMN = None


# ======================================================================================================================
# Output configuration
# ======================================================================================================================

# Output dataset file
OUTPUT_FILE = ROOT_DIR + 'data/output.csv'

# Output CSV file row separator
OUTPUT_SEPARATOR = ';'

# Name of the column with the new categories
INFERRED_COLUMN = 'inferred_category'
