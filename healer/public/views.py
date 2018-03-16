# -*- coding: utf-8 -*-

"""
Public section
"""

import os
import json

from flask import Blueprint, render_template, request, Response
import pandas as pd

from ..utils import NumpyJsonEncoder, check_config, list_is_true, str_to_list, translate_separator

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET'])
def index():
    """Home page"""
    return render_template('index.html')


@blueprint.route('/start/', methods=['POST'])
def start():
    """Funcion tha checks the configurations and get the available classes"""

    # Params preprocessing
    json_data = request.get_json()
    input_file = json_data['input_file'].strip(' ')
    separator = translate_separator(json_data['separator'].strip(' '))
    columns_to_show = str_to_list(json_data['columns_to_show'])
    help_column =  json_data['help_column'].strip(' ')
    output_file = json_data['output_file'].strip(' ')
    class_column = json_data['class_column'].strip(' ')
    classes = str_to_list(json_data['classes'])

    errors = check_config(input_file, separator, columns_to_show, help_column, output_file, class_column, classes)

    if len(errors) > 0:
        return json.dumps({'errors': errors}, cls=NumpyJsonEncoder)
    else:
        input_df = pd.read_csv(input_file, sep=separator, encoding='utf-8')
        total_rows = input_df.shape[0]

        if help_column != '':
            classes = list(input_df[help_column].unique())
        else:
            classes = str_to_list(classes)
        return json.dumps({'classes': classes, 'total_rows': total_rows}, cls=NumpyJsonEncoder)


@blueprint.route('/get_row/', methods=['GET'])
def get_row():
    """Get the n specified of the dataset"""

    # Params preprocessing
    input_file = request.args.get('input_file', type=str).strip(' ')
    separator = translate_separator(request.args.get('separator', type=str).strip(' '))
    columns_to_show = str_to_list(request.args.get('columns_to_show', type=str))
    help_column = request.args.get('help_column', type=str).strip(' ')
    output_file = request.args.get('output_file', type=str).strip(' ')
    class_column = request.args.get('class_column', type=str).strip(' ')
    n_row = request.args.get('n_row', type=int)

    input_df = pd.read_csv(input_file, sep=separator, encoding='utf-8')

    # Finish classification
    if n_row == input_df.shape[0]:
        return json.dumps({'finish': 1}, cls=NumpyJsonEncoder)

    # If an output file has been started it will continue with it
    existing_control_file = False
    partial_output_file = output_file.split('.')[0] + '_partial.csv'
    if n_row == 0 and os.path.exists(partial_output_file):
        existing_control_file = True
        output_df = pd.read_csv(partial_output_file, sep=separator, encoding='utf-8')
        if class_column in output_df.columns:
            output_df.drop(class_column, axis=1, inplace=True)
            n_row = output_df.shape[0] - 1
            input_row = input_df.iloc[n_row]
            output_row = output_df.iloc[n_row]

            # Search last row classified
            while not list_is_true(list(input_row == output_row)) and n_row < input_df.shape[0]:
                n_row += 1
                input_row = input_df.iloc[n_row]
            n_row += 1

    if n_row > input_df.shape[0]:
        return json.dumps({'errors': ['row index ({}) is greater than dataframe shape'.format(n_row)]},
                          cls=NumpyJsonEncoder)

    # Get required row information
    row = {column: input_df.iloc[n_row][column] for column in columns_to_show}
    if help_column in input_df.columns:
        row[help_column] = input_df.iloc[n_row][help_column]

    return json.dumps({'row': row, 'n_row': n_row, 'finish': 0,
                       'existing_control_file': int(existing_control_file)}, cls=NumpyJsonEncoder)


@blueprint.route('/save_row/', methods=['POST'])
def save_row():
    """Save a new categorized row in the final dataset"""

    # Params preprocessing
    json_data = request.get_json()
    input_file = request.args.get('input_file', type=str).strip(' ')
    separator = translate_separator(request.args.get('separator', type=str).strip(' '))
    output_file = request.args.get('output_file', type=str).strip(' ')
    class_column = request.args.get('class_column', type=str).strip(' ')
    n_row = request.args.get('n_row', type=int)
    selected_class = request.args.get('selected_class', type=str).strip(' ')

    input_df = pd.read_csv(input_file, sep=separator, encoding='utf-8')
    partial_output_file = output_file.split('.')[0] + '_partial.csv'

    # Load or create Pandas data-frame
    if os.path.exists(partial_output_file):
        output_df = pd.read_csv(partial_output_file, sep=separator, encoding='utf-8')
        columns = output_df.columns.tolist()
    else:
        columns = input_df.columns.tolist()
        columns.append(class_column)
        output_df = pd.DataFrame(columns=columns)

    # Add classified row to the data-frame
    row = {column: input_df.iloc[n_row][column] for column in input_df.columns.tolist()}
    # Overwrite user-edited attrs
    for attr in json_data['row']:
        row[attr] = json_data['row'][attr]
    row[class_column] = selected_class
    row = pd.DataFrame([row], columns=columns)
    output_df = output_df.append(row)

    # Save results
    if n_row == input_df.shape[0] - 1:
        output_df.to_csv(output_file, sep=separator, encoding='utf-8', index=False)
        os.remove(partial_output_file)
    else:
        output_df.to_csv(partial_output_file, sep=separator, encoding='utf-8', index=False)

    return Response(status=200)


@blueprint.route('/get_previous_row/', methods=['GET'])
def get_previous_row():
    """Get previous row undoing the last action"""

    # Params preprocessing
    input_file = request.args.get('input_file', type=str).strip(' ')
    separator = translate_separator(request.args.get('separator', type=str).strip(' '))
    columns_to_show = str_to_list(request.args.get('columns_to_show', type=str))
    help_column = request.args.get('help_column', type=str).strip(' ')
    output_file = request.args.get('output_file', type=str).strip(' ')
    class_column = request.args.get('class_column', type=str).strip(' ')
    n_row = request.args.get('n_row', type=int)

    if n_row >= 0:
        input_df = pd.read_csv(input_file, sep=separator, encoding='utf-8')
        input_row = input_df.iloc[n_row]
        partial_output_file = output_file.split('.')[0] + '_partial.csv'
        if os.path.exists(partial_output_file):
            output_df = pd.read_csv(partial_output_file, sep=separator, encoding='utf-8')

            # If the last row is in the output data-frame it has to be removed (the row didn't be ignored)
            aux_output_df = output_df.copy()
            aux_output_df.drop(class_column, axis=1, inplace=True)
            output_row = aux_output_df.iloc[aux_output_df.shape[0] - 1]
            if list_is_true(list(input_row == output_row)):
                output_df = output_df.drop(aux_output_df.shape[0] - 1)
            if output_df.shape[0] == 0:
                os.remove(partial_output_file)
            else:
                output_df.to_csv(partial_output_file, sep=separator, encoding='utf-8', index=False)

        # Get required row information
        row = {column: input_row[column] for column in columns_to_show}
        if help_column in input_df.columns:
            row[help_column] = input_row[help_column]
        return json.dumps({'row': row, 'n_row': n_row}, cls=NumpyJsonEncoder)

    else:
        return json.dumps({'errors': ['Row 0 doesn\'t have previous']}, cls=NumpyJsonEncoder)


