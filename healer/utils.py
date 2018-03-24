# -*- coding: utf-8 -*-

"""
Helper utilities
"""

import os.path
import re
import json

import pandas as pd
import numpy as np


class NumpyJsonEncoder(json.JSONEncoder):
    """
    JSON serializers have some problems with numpy types
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyJsonEncoder, self).default(obj)


def check_config(input_file, separator, columns_to_show, help_column, output_file, class_column, classes):
    """
    Function that checks the configuration specified by the user
    :param input_file: CSV input path
    :param separator: CSV separator (, or ;)
    :param columns_to_show: List of CSV columns to show in the interface
    :param help_column: Default class column
    :param output_file: CSV output path
    :param class_column: New column class
    :param classes: List of available classes
    :return errors: {list}
    """

    errors = []
    if not os.path.exists(input_file):
        errors.append('Input file doesn\'t exist.')
    if separator == '':
        errors.append('Separator not specified.')
    input_df = None
    if len(errors) == 0:
        input_df = pd.read_csv(input_file, sep=separator, encoding='utf-8')
        if help_column != '':
            if help_column not in input_df.columns:
                errors.append('Help column does not exist in the CSV file.')
        elif len(classes) == 0:
            errors.append('There are not defined classes.')
    if columns_to_show is None or len(columns_to_show) == 0:
        errors.append('Columns to show not specified.')
    else:
        if input_df is not None:
            for column in columns_to_show:
                if column not in input_df.columns:
                    errors.append('{} column does not exist in the CSV file.'.format(column))
    if class_column == '':
        errors.append('You must to specify a class column')
    if input_df is not None:
        if class_column in input_df.columns:
            errors.append('Column {} already exists in the CSV file.'.format(class_column))
    if output_file == '':
        errors.append('You must to specify an output file')
    if os.path.exists(output_file):
        errors.append('Looks like exists a finished output file. Drop it if you want to start again.')
    if not os.path.isdir(os.path.dirname(output_file)):
        errors.append('Output path doesn\'t exist')
    if input_file == output_file:
        errors.append('Input and output must be different files')
    partial_output_file = output_file.split('.')[0] + '_partial.csv'
    if os.path.exists(partial_output_file):
        output_df = pd.read_csv(partial_output_file, sep=separator, encoding='utf-8')
        if class_column not in output_df.columns:
            errors.append('Looks like there is a control file saved and'
                          ' class column specified is not an existing column in it.')
    return errors


def list_is_true(list):
    """
    Function that checks if all the elements of the list are True
    :param list: {list}
    :return: {boolean}
    """
    for elem in list:
        if not elem:
            return False
    return True


def str_to_list(str_list):
    """
    Function that casts an string with comma separated classes in a list of string
    :return: {list}
    """
    if str_list in ['', ' ']:
        return []
    slices = str_list.split(',')
    return [slice.strip(' ') for slice in slices]


def translate_separator(separator):
    """
    Translate string separators to their symbol
    :param separator: {str}
    :return: {str}
    """
    if separator == 'semicolon':
        return ';'
    elif separator == 'coma':
        return ','


def get_partial_file(output_file):
    """
    Function that construct the path to the output_partial path
    :param output_file: Final output path
    :return: Partial output path
    """
    return 'data/{}'.format(os.path.basename(output_file).split('.')[0] + '_partial.csv')


def get_doubts_file(output_file):
    """
    Function that construct the path to the output_partial path
    :param output_file: Final output path
    :return: Partial output path
    """
    slices = output_file.split('/')
    return 'data/{}'.format(os.path.basename(output_file).split('.')[0] + '_doubts.csv')
