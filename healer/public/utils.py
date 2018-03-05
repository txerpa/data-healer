# -*- coding: utf-8 -*-

"""
Python util functions
"""

import os.path

import pandas as pd

import conf


def check_confs():
    """
    Function that checks the configuration specified by the user
    :return errors: {list}
    """
    errors = []
    if not os.path.exists(conf.INPUT_FILE):
        errors.append('Input file doesn\'t exist.')
    if conf.INPUT_SEPARATOR == '':
        errors.append('Input separator not specified.')
    df = None
    if len(errors) == 0:
        df = pd.read_csv(conf.INPUT_FILE, sep=conf.INPUT_SEPARATOR, encoding='utf-8')
        if conf.HELP_COLUMN is not None:
            if conf.HELP_COLUMN not in df.columns:
                errors.append('Help column does not exist in the CSV file.')
    if conf.OUTPUT_SEPARATOR == '':
        errors.append('Output separator not specified.')
    if len(conf.COLUMNS_TO_SHOW) == 0:
        errors.append('Columns to show not specified.')
    else:
        if df is not None:
            for column in conf.COLUMNS_TO_SHOW:
                if column not in df.columns:
                    errors.append('{} column does not exist in the CSV file.'.format(column))
    if df is not None:
        if conf.INFERRED_COLUMN in df.columns:
            errors.append('Column {} already exists in the CSV file.'.format(conf.INFERRED_COLUMN))
    slices = conf.OUTPUT_FILE.split('/')
    slices = slices[0:len(slices)-1]
    if not os.path.isdir('/' + '/'.join(slices)):
        errors.append('Output path does not exist')
    return errors

