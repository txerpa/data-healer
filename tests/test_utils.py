# -*- coding: utf-8 -*-

"""Test utils"""

import os
import unittest

import pandas as pd

from healer.app import create_app
from healer.settings import TestConfig
from healer.utils import verify_confs, list_is_true
import conf


class ViewTests(unittest.TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        self.app = app.test_client()

        self.df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.df.to_csv('data/input_test.csv', sep=';', encoding='utf-8')

    def tearDown(self):
        os.remove('data/input_test.csv')

    def test_no_input_file(self):
        conf.INPUT_FILE = 'daa/input_test.csv'
        errors = verify_confs()
        self.assertTrue('Input file doesn\'t exist.' in errors)

    def test_input_file(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        errors = verify_confs()
        self.assertFalse('Input file doesn\'t exist.' in errors)

    def test_no_separator(self):
        conf.CSV_SEPARATOR = None
        errors = verify_confs()
        self.assertTrue('Separator not specified.' in errors)

    def test_separator(self):
        conf.CSV_SEPARATOR = ';'
        errors = verify_confs()
        self.assertFalse('Separator not specified.' in errors)

    def test_no_help_column(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = 'col3'
        errors = verify_confs()
        self.assertTrue('Help column does not exist in the CSV file.' in errors)

    def test_help_column(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = 'col2'
        errors = verify_confs()
        self.assertFalse('Help column does not exist in the CSV file.' in errors)

    def test_no_categories(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = []
        errors = verify_confs()
        self.assertTrue('There are not defined categories.' in errors)

    def test_categories(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        errors = verify_confs()
        self.assertFalse('There are not defined categories.' in errors)

    def test_no_columns_to_show(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = None
        errors = verify_confs()
        self.assertTrue('Columns to show not specified.' in errors)

    def test_columns_to_show(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col1', ]
        errors = verify_confs()
        self.assertFalse('Columns to show not specified.' in errors)

    def test_column_to_show_no_exist(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col3', ]
        errors = verify_confs()
        self.assertTrue('col3 column does not exist in the CSV file.' in errors)

    def test_column_to_show_exists(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col2', ]
        errors = verify_confs()
        self.assertFalse('col2 column does not exist in the CSV file.' in errors)

    def test_inferred_column_in_columns(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col2', ]
        conf.INFERRED_COLUMN = 'col2'
        errors = verify_confs()
        self.assertTrue('Column col2 already exists in the CSV file.' in errors)

    def test_inferred_column_not_in_columns(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col2', ]
        conf.INFERRED_COLUMN = 'col3'
        errors = verify_confs()
        self.assertFalse('Column col3 already exists in the CSV file.' in errors)

    def test_output_file_exists(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col2', ]
        conf.INFERRED_COLUMN = 'col3'
        conf.OUTPUT_FILE = 'data/output_test.csv'
        self.df.to_csv('data/output_test.csv', sep=';', encoding='utf-8')
        errors = verify_confs()
        self.assertTrue('Looks like exists a finished output file. Drop it if you want to start again.' in errors)
        os.remove('data/output_test.csv')

    def test_output_file_no_exists(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col2', ]
        conf.INFERRED_COLUMN = 'col3'
        conf.OUTPUT_FILE = 'data/output_test.csv'
        errors = verify_confs()
        self.assertFalse('Looks like exists a finished output file. Drop it if you want to start again.' in errors)

    def test_output_path_no_exists(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col2', ]
        conf.INFERRED_COLUMN = 'col3'
        conf.OUTPUT_FILE = 'daa/output_test.csv'
        errors = verify_confs()
        self.assertTrue('Output path does not exist' in errors)

    def test_output_path_exists(self):
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.CSV_SEPARATOR = ';'
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', ]
        conf.COLUMNS_TO_SHOW = ['col2', ]
        conf.INFERRED_COLUMN = 'col3'
        conf.OUTPUT_FILE = conf.ROOT_DIR + 'data/output_test.csv'
        errors = verify_confs()
        self.assertFalse('Output path does not exist' in errors)

    def test_list_is_true(self):
        self.assertTrue(list_is_true([True, True, True]))

    def test_list_is_not_true(self):
        self.assertFalse(list_is_true([True, False, True]))
