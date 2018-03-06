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
INPUT_FILE = ROOT_DIR + 'data/N6272_D2018-03-02_categorized.csv'

# Input CSV file row separator
INPUT_SEPARATOR = ';'

# Columns to show in the screen (information that the user needs to categorize the row)
COLUMNS_TO_SHOW = ['original_messages', 'authors', ]

# If this column is not None the category of this column will be used as a clue for the user
# (this column could have been inferred by an unsupervised learning algorithm)
HELP_COLUMN = None

# If HELP_COLUMN is not provided these are the categories provided to the user in the interface
CATEGORIES = ['category1', 'category2', 'category3', 'category4']


# ======================================================================================================================
# Output configuration
# ======================================================================================================================

# Output dataset file
OUTPUT_FILE = ROOT_DIR + 'data/output.csv'

# Output CSV file row separator
OUTPUT_SEPARATOR = ';'

# Name of the column with the new categories
INFERRED_COLUMN = 'inferred_category'
