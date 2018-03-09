# -*- coding: utf-8 -*-

"""
Public section
"""

import os
import json

from flask import Blueprint, render_template, request, Response
import pandas as pd

from ..utils import NumpyJsonEncoder, check_config, list_is_true, str_to_list, translate_separator, remove_spaces

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET'])
def index():
    """Home page"""
    return render_template('index.html')


@blueprint.route('/start/', methods=['POST'])
def start():
    """Funcion tha checks the configurations and get the available classes"""
    json_data = request.get_json()
    separator = translate_separator(json_data['separator'])
    errors = check_config(json_data['input_file'], separator, str_to_list(json_data['columns_to_show']),
                          json_data['help_column'], json_data['output_file'], json_data['class_column'],
                          str_to_list(json_data['classes']))
    if len(errors) > 0:
        return json.dumps({'errors': errors}, cls=NumpyJsonEncoder)
    else:
        input_df = pd.read_csv(json_data['input_file'], sep=separator, encoding='utf-8')
        total_rows = input_df.shape[0]

        if json_data['help_column'] != '':
            classes = list(input_df[json_data['help_column']].unique())
        else:
            classes = str_to_list(json_data['classes'])
        return json.dumps({'classes': classes, 'total_rows': total_rows}, cls=NumpyJsonEncoder)


@blueprint.route('/get_row/', methods=['GET'])
def get_row():
    """Get the next row of the dataset"""
    input_file = remove_spaces(request.args.get('input_file', type=str))
    separator = translate_separator(remove_spaces(request.args.get('separator', type=str)))
    columns_to_show = str_to_list(remove_spaces(request.args.get('columns_to_show', type=str)))
    help_column = remove_spaces(request.args.get('help_column', type=str))
    output_file = remove_spaces(request.args.get('output_file', type=str))
    class_column = remove_spaces(request.args.get('class_column', type=str))
    n_row = request.args.get('n_row', type=int)

    input_df = pd.read_csv(input_file, sep=separator, encoding='utf-8')

    # Finish
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
            while not list_is_true(list(input_row == output_row)) and n_row < input_df.shape[0]:
                n_row += 1
                input_row = input_df.iloc[n_row]
            n_row += 1

    if n_row > input_df.shape[0]:
        return json.dumps({'errors': ['row index ({}) is greater than dataframe shape'.format(n_row)]},
                          cls=NumpyJsonEncoder)

    row = {column: input_df.iloc[n_row][column] for column in columns_to_show}
    if help_column in input_df.columns:
        row[help_column] = input_df.iloc[n_row][help_column]

    return json.dumps({'row': row, 'n_row': n_row, 'finish': 0, 'existing_control_file': int(existing_control_file)},
                      cls=NumpyJsonEncoder)


@blueprint.route('/post_row/', methods=['POST'])
def post_row():
    """Post a new row in the final dataset"""
    json_data = request.get_json()
    separator = translate_separator(json_data['separator'])
    input_df = pd.read_csv(json_data['input_file'], sep=separator, encoding='utf-8')
    partial_output_file = json_data['output_file'].split('.')[0] + '_partial.csv'

    if os.path.exists(partial_output_file):
        output_df = pd.read_csv(partial_output_file, sep=separator, encoding='utf-8')
        columns = output_df.columns.tolist()
    else:
        columns = input_df.columns.tolist()
        columns.append(json_data['class_column'])
        output_df = pd.DataFrame(columns=columns)

    row = {column: input_df.iloc[json_data['n_row']][column] for column in input_df.columns.tolist()}
    row[json_data['class_column']] = json_data['selected_class']
    row = pd.DataFrame([row], columns=columns)
    output_df = output_df.append(row)

    if json_data['n_row'] == input_df.shape[0] - 1:
        output_df.to_csv(json_data['output_file'], sep=separator, encoding='utf-8', index=False)
        os.remove(partial_output_file)
    else:
        output_df.to_csv(partial_output_file, sep=separator, encoding='utf-8', index=False)

    return Response(status=200)

