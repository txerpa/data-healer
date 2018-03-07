# -*- coding: utf-8 -*-

"""
Helper utilities
"""

import os.path

import pandas as pd

import conf


def verify_confs():
    """
    Function that checks the configuration specified by the user
    :return errors: {list}
    """
    errors = []
    if not os.path.exists(conf.INPUT_FILE):
        errors.append('Input file doesn\'t exist.')
    if conf.CSV_SEPARATOR == '':
        errors.append('Separator not specified.')
    input_df = None
    if len(errors) == 0:
        input_df = pd.read_csv(conf.INPUT_FILE, sep=conf.CSV_SEPARATOR, encoding='utf-8')
        if conf.HELP_COLUMN is not None:
            if conf.HELP_COLUMN not in input_df.columns:
                errors.append('Help column does not exist in the CSV file.')
        elif len(conf.CATEGORIES) == 0:
            errors.append('There are not defined categories.')
    if len(conf.COLUMNS_TO_SHOW) == 0:
        errors.append('Columns to show not specified.')
    else:
        if input_df is not None:
            for column in conf.COLUMNS_TO_SHOW:
                if column not in input_df.columns:
                    errors.append('{} column does not exist in the CSV file.'.format(column))
    if input_df is not None:
        if conf.INFERRED_COLUMN in input_df.columns:
            errors.append('Column {} already exists in the CSV file.'.format(conf.INFERRED_COLUMN))
    if os.path.exists(conf.OUTPUT_FILE):
        errors.append('Looks like exists a finished output file. Drop it if you want to start again.')
    slices = conf.OUTPUT_FILE.split('/')
    slices = slices[0:len(slices)-1]
    if not os.path.isdir('/' + '/'.join(slices)):
        errors.append('Output path does not exist')
    return errors


def list_is_true(list):
    """
    Function that checks if all the elements of the list are True
    :param list:
    """
    for elem in list:
        if not elem:
            return False
    return True
