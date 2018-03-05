# -*- coding: utf-8 -*-

"""
Public section, including homepage and signup.
"""

from flask import Blueprint, render_template, jsonify, request
import pandas as pd

import conf
from .utils import check_confs

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET'])
def home():
    """Home page."""
    info = {
        'input_file': conf.INPUT_FILE,
        'input_separator': conf.INPUT_SEPARATOR,
        'columns_to_show': conf.COLUMNS_TO_SHOW,
        'help_column': conf.HELP_COLUMN,
        'output_file': conf.OUTPUT_FILE,
        'output_separator': conf.OUTPUT_SEPARATOR,
        'inferred_column': conf.INFERRED_COLUMN
    }
    return render_template('home.html', **info)


@blueprint.route('/about/', methods=['GET'])
def about():
    """About page."""
    return render_template('about.html')


@blueprint.route('/get_row/', methods=['GET'])
def get_row():
    """Get the next row of the dataset"""
    errors = check_confs()
    if len(errors) > 0:
        return jsonify({'errors': errors})
    df = pd.read_csv(conf.INPUT_FILE, sep=conf.INPUT_SEPARATOR, encoding='utf-8')
    row = request.args.get('row', type=int)
    if row > df.shape[0]:
        return jsonify({'errors': ['row index ({}) is greater than dataframe shape'.format(row)]})
    return jsonify({'row': {column: df.iloc[row][column] for column in conf.COLUMNS_TO_SHOW}})

