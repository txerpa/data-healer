# -*- coding: utf-8 -*-

"""
Helper utilities
"""

import os.path

from flask import flash
import pandas as pd

import conf


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def verify_confs():
    """
    Function that checks the configuration specified by the user
    :return errors: {list}
    """
    errors = []
    if not os.path.exists(conf.INPUT_FILE):
        errors.append('Input file doesn\'t exist.')
    if conf.INPUT_SEPARATOR == '':
        errors.append('Input separator not specified.')
    input_df = None
    if len(errors) == 0:
        input_df = pd.read_csv(conf.INPUT_FILE, sep=conf.INPUT_SEPARATOR, encoding='utf-8')
        if conf.HELP_COLUMN is not None:
            if conf.HELP_COLUMN not in input_df.columns:
                errors.append('Help column does not exist in the CSV file.')
    if conf.OUTPUT_SEPARATOR == '':
        errors.append('Output separator not specified.')
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
    slices = conf.OUTPUT_FILE.split('/')
    slices = slices[0:len(slices)-1]
    if not os.path.isdir('/' + '/'.join(slices)):
        errors.append('Output path does not exist')
    return errors
