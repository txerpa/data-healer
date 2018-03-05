# -*- coding: utf-8 -*-

"""
Application configuration file
In this file the user must specify some options for the automatization of the categorization task
"""

# Input dataset file
INPUT_FILE = 'data/input.csv'

# Input CSV file row separator
INPUT_SEPARATOR = ';'

# Columns to show in the screen (information that the user needs to categorize the row)
COLUMNS_TO_SHOW = ['original_messages', ]

# If this column is not None the category of this column will be used as a clue for the user
# (this column could have been inferred by an unsupervised learning algorithm)
HELP_COLUMN = None


# Output
OUTPUT_FILE = 'data/output.csv'

# Name of the column with the new categories
INFERRED_COLUMN = 'category'
