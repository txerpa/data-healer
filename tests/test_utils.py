# -*- coding: utf-8 -*-

"""Test utils"""

import os
import unittest

import pandas as pd

from healer.app import create_app
from healer.settings import TestConfig
from healer.utils import check_config, list_is_true, str_to_list, translate_separator, remove_spaces


class ViewTests(unittest.TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        self.app = app.test_client()

        self.df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.df.to_csv('input_test.csv', sep=';', encoding='utf-8')

        self.separator = 'semicolon'
        self.input_file = 'input_test.csv'
        self.columns_to_show = ['col1', ]
        self.help_column = 'col2'
        self.classes = 'A, B, C'
        self.output_file = 'output_test.csv'
        self.class_column = 'classes'

    def tearDown(self):
        if os.path.exists('input_test.csv'):
            os.remove('input_test.csv')
        if os.path.exists('output_test.csv'):
            os.remove('output_test.csv')
        if os.path.exists('output_test_partial.csv'):
            os.remove('output_test_partial.csv')

    def test_config_ok(self):
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, self.output_file, self.class_column, self.classes)
        self.assertTrue(len(errors) == 0)

    def test_no_input_file(self):
        input_file = 'inputt_test.csv'
        errors = check_config(input_file, self.separator, self.columns_to_show,
                              self.help_column, self.output_file, self.class_column, self.classes)
        self.assertTrue('Input file doesn\'t exist.' in errors)

    def test_no_separator(self):
        separator = ''
        errors = check_config(self.input_file, separator, self.columns_to_show,
                              self.help_column, self.output_file, self.class_column, self.classes)
        self.assertTrue('Separator not specified.' in errors)

    def test_no_help_column(self):
        help_column = 'col3'
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              help_column, self.output_file, self.class_column, self.classes)
        self.assertTrue('Help column does not exist in the CSV file.' in errors)

    def test_no_classes(self):
        help_column = ''
        classes = []
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              help_column, self.output_file, self.class_column, classes)
        self.assertTrue('There are not defined classes.' in errors)

    def test_no_columns_to_show(self):
        columns_to_show = []
        errors = check_config(self.input_file, translate_separator(self.separator), columns_to_show,
                              self.help_column, self.output_file, self.class_column, self.classes)
        self.assertTrue('Columns to show not specified.' in errors)

    def test_column_to_show_no_exist(self):
        columns_to_show = ['col3', ]
        errors = check_config(self.input_file, translate_separator(self.separator), columns_to_show,
                              self.help_column, self.output_file, self.class_column, self.classes)
        self.assertTrue('col3 column does not exist in the CSV file.' in errors)

    def test_no_class_column(self):
        class_column = ''
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, self.output_file, class_column, self.classes)
        self.assertTrue('You must to specify a class column' in errors)

    def test_class_column_in_columns(self):
        class_column = 'col2'
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, self.output_file, class_column, self.classes)
        self.assertTrue('Column col2 already exists in the CSV file.' in errors)

    def test_no_output_file(self):
        output_file = ''
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, output_file, self.class_column, self.classes)
        self.assertTrue('You must to specify an output file' in errors)

    def test_output_file_exists(self):
        output_file = 'output_test.csv'
        self.df.to_csv('output_test.csv', sep=';', encoding='utf-8')
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, output_file, self.class_column, self.classes)
        self.assertTrue('Looks like exists a finished output file. Drop it if you want to start again.' in errors)

    def test_output_path_no_exists(self):
        output_file = 'data/output_test.csv'
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, output_file, self.class_column, self.classes)
        self.assertTrue('Output path doesn\'t exist' in errors)

    def test_input_output_same(self):
        output_file = 'input_test.csv'
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, output_file, self.class_column, self.classes)
        self.assertTrue('Input and output must be different files' in errors)

    def test_input_output_not_same(self):
        output_file = 'output_test.csv'
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, output_file, self.class_column, self.classes)
        self.assertFalse('Input and output must be different files' in errors)

    def test_control_file_saved(self):
        output_file = 'output_test.csv'
        self.df.to_csv('output_test_partial.csv', sep=';', encoding='utf-8')
        errors = check_config(self.input_file, translate_separator(self.separator), self.columns_to_show,
                              self.help_column, output_file, self.class_column, self.classes)
        self.assertTrue('Looks like there is a control file saved and'
                        ' class column specified is not an existing column in it.' in errors)

    def test_list_is_true(self):
        self.assertTrue(list_is_true([True, True, True]))

    def test_list_is_not_true(self):
        self.assertFalse(list_is_true([True, False, True]))

    def test_str_to_list(self):
        self.assertEqual(len(str_to_list(self.classes)), 3)

    def test_translate_separator(self):
        self.assertEqual(translate_separator('semicolon'), ';')
        self.assertEqual(translate_separator('coma'), ',')

    def test_remove_spaces(self):
        self.assertEqual(remove_spaces(' sf  fgs  '), 'sffgs')
