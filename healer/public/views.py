# -*- coding: utf-8 -*-

"""
Public section, including homepage and signup
"""

import os.path

from flask import Blueprint, render_template, jsonify, request, Response
import pandas as pd

import conf
from ..utils import verify_confs, list_is_true

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET'])
def home():
    """Home page"""
    info = {
        'separator': conf.CSV_SEPARATOR,
        'input_file': conf.INPUT_FILE,
        'columns_to_show': conf.COLUMNS_TO_SHOW,
        'help_column': conf.HELP_COLUMN,
        'output_file': conf.OUTPUT_FILE,
        'output_file_exists': int(os.path.exists(conf.OUTPUT_FILE)),
        'inferred_column': conf.INFERRED_COLUMN
    }
    return render_template('home.html', **info)


@blueprint.route('/about/', methods=['GET'])
def about():
    """About page"""
    return render_template('about.html')


@blueprint.route('/check_confs/', methods=['GET'])
def check_confs():
    """Funcion tha checks the configurations writed in conf.py by the user"""
    errors = verify_confs()
    return jsonify({'errors': errors})


@blueprint.route('/get_row/', methods=['GET'])
def get_row():
    """Get the next row of the dataset"""
    input_df = pd.read_csv(conf.INPUT_FILE, sep=conf.CSV_SEPARATOR, encoding='utf-8')
    n_row = request.args.get('n_row', type=int)

    # Finish
    if n_row == input_df.shape[0]:
        return jsonify({'finish': 1})

    # If an output file has been started it will continue with it
    if n_row == 0 and os.path.exists(conf.OUTPUT_FILE):
        output_df = pd.read_csv(conf.OUTPUT_FILE, sep=conf.CSV_SEPARATOR, encoding='utf-8')
        if conf.INFERRED_COLUMN in output_df.columns.tolist():
            output_df.drop(conf.INFERRED_COLUMN, axis=1, inplace=True)
            n_row = output_df.shape[0] - 1
            input_row = input_df.iloc[n_row]
            output_row = output_df.iloc[n_row]
            while not list_is_true(list(input_row == output_row)) and n_row < input_df.shape[0]:
                n_row += 1
                input_row = input_df.iloc[n_row]
            n_row += 1

    if n_row > input_df.shape[0]:
        return jsonify({'errors': ['row index ({}) is greater than dataframe shape'.format(n_row)]})
    return jsonify({'row': {column: input_df.iloc[n_row][column] for column in conf.COLUMNS_TO_SHOW},
                    'n_row': n_row, 'finish': 0})


@blueprint.route('/get_categories/', methods=['GET'])
def get_categories():
    """Get the categories availables for categorize a row"""
    input_df = pd.read_csv(conf.INPUT_FILE, sep=conf.CSV_SEPARATOR, encoding='utf-8')
    total_rows = input_df.shape[0]

    if conf.HELP_COLUMN is not None:
        categories = list(input_df[conf.HELP_COLUMN].unique())
    else:
        categories = conf.CATEGORIES
    return jsonify({'categories': categories, 'total_rows': total_rows})


@blueprint.route('/post_row/', methods=['POST'])
def post_row():
    """Post a new row in the final dataset"""
    json = request.get_json()
    input_df = pd.read_csv(conf.INPUT_FILE, sep=conf.CSV_SEPARATOR, encoding='utf-8')
    partial_output_file = conf.OUTPUT_FILE.split('.')[0] + '_partial.csv'

    if os.path.exists(partial_output_file):
        output_df = pd.read_csv(partial_output_file, sep=conf.CSV_SEPARATOR, encoding='utf-8')
        columns = output_df.columns.tolist()
    else:
        columns = input_df.columns.tolist()
        columns.append(conf.INFERRED_COLUMN)
        output_df = pd.DataFrame(columns=columns)

    row = {column: input_df.iloc[json['n_row']][column] for column in input_df.columns.tolist()}
    row[conf.INFERRED_COLUMN] = json['category']
    row = pd.DataFrame([row], columns=columns)
    output_df = output_df.append(row)

    if json['n_row'] == input_df.shape[0] - 1:
        output_df.to_csv(conf.OUTPUT_FILE, sep=conf.CSV_SEPARATOR, encoding='utf-8', index=False)
        os.remove(partial_output_file)
    else:
        output_df.to_csv(partial_output_file, sep=conf.CSV_SEPARATOR, encoding='utf-8', index=False)

    return Response(status=200)

