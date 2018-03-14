# -*- coding: utf-8 -*-

"""Test urls"""

import os
import json
import unittest

import pandas as pd

from healer.app import create_app
from healer.settings import TestConfig


class ViewTests(unittest.TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        self.app = app.test_client()

        self.df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.df.to_csv('input_test.csv', sep=';', encoding='utf-8')

        self.separator = 'semicolon'
        self.input_file = 'input_test.csv'
        self.columns_to_show = 'col1'
        self.help_column = ''
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

    def test_home(self):
        response = self.app.get('/')
        self.assertNotEqual(response.status_code, 404)

    def test_good_start(self):
        data = {
            'input_file': self.input_file,
            'separator': self.separator,
            'columns_to_show': self.columns_to_show,
            'help_column': self.help_column,
            'output_file': self.output_file,
            'class_column': self.class_column,
            'classes': self.classes,
        }
        response = self.app.post('/start/', data=json.dumps(data), content_type='application/json')
        self.assertNotEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(('classes' in data))
        self.assertTrue(('total_rows' in data))

    def test_bad_start(self):
        data = {
            'input_file': 'bad_input.csv',
            'separator': '',
            'columns_to_show': 'D',
            'help_column': 'D',
            'output_file': 'bad_output.csv',
            'class_column': 'C',
            'classes': '',
        }
        response = self.app.post('/start/', data=json.dumps(data), content_type='application/json')
        self.assertNotEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(('errors' in data))
        self.assertFalse(('classes' in data))
        self.assertFalse(('total_rows' in data))

    def test_get_row(self):
        response = self.app.get('/get_row/?input_file={}&separator={}&columns_to_show={}'
                                '&help_column={}&output_file={}&class_column={}&n_row={}' \
                                .format(self.input_file, self.separator, self.columns_to_show,
                                        self.help_column, self.output_file, self.class_column, 0))
        self.assertNotEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['finish'], 0)
        self.assertTrue('row' in data)

    def test_get_last_row(self):
        response = self.app.get('/get_row/?input_file={}&separator={}&columns_to_show={}'
                                '&help_column={}&output_file={}&class_column={}&n_row={}' \
                                .format(self.input_file, self.separator, self.columns_to_show,
                                        self.help_column, self.output_file, self.class_column, 2))
        self.assertNotEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['finish'], 1)
        self.assertFalse('row' in data)

    def test_get_error_row(self):
        response = self.app.get('/get_row/?input_file={}&separator={}&columns_to_show={}'
                                '&help_column={}&output_file={}&class_column={}&n_row={}' \
                                .format(self.input_file, self.separator, self.columns_to_show,
                                        self.help_column, self.output_file, self.class_column, 3))
        self.assertNotEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue('errors' in data)

    def test_save_row(self):
        data = {
            'input_file': self.input_file,
            'separator': self.separator,
            'output_file': self.output_file,
            'class_column': self.class_column,
            'n_row': 0,
            'selected_class': 'A',
        }
        self.assertFalse(os.path.exists('output_test_partial.csv'))
        response = self.app.post('/save_row/', data=json.dumps(data), content_type='application/json')
        self.assertNotEqual(response.status_code, 404)
        self.assertTrue(os.path.exists('output_test_partial.csv'))

    def test_save_last_row(self):
        data = {
            'input_file': self.input_file,
            'separator': self.separator,
            'output_file': self.output_file,
            'class_column': self.class_column,
            'n_row': 0,
            'selected_class': 'A',
        }
        self.assertFalse(os.path.exists('output_test.csv'))
        self.app.post('/save_row/', data=json.dumps(data), content_type='application/json')
        data['n_row'] = 1
        response = self.app.post('/save_row/', data=json.dumps(data), content_type='application/json')
        self.assertNotEqual(response.status_code, 404)
        self.assertTrue(os.path.exists('output_test.csv'))

    def test_get_previous_row_saved(self):
        self.test_save_row()
        df = pd.read_csv('output_test_partial.csv', sep=';', encoding='utf-8')
        self.assertEqual(df.shape[0], 1)
        response = self.app.get('/get_previous_row/?input_file={}&separator={}&columns_to_show={}'
                                '&help_column={}&output_file={}&class_column={}&n_row={}' \
                                .format(self.input_file, self.separator, self.columns_to_show,
                                        self.help_column, self.output_file, self.class_column, 0))
        self.assertNotEqual(response.status_code, 404)
        self.assertFalse(os.path.exists('output_test_partial.csv'))

    def test_get_previous_row_ignored(self):
        self.test_save_row()
        df = pd.read_csv('output_test_partial.csv', sep=';', encoding='utf-8')
        self.assertEqual(df.shape[0], 1)
        response = self.app.get('/get_previous_row/?input_file={}&separator={}&columns_to_show={}'
                                '&help_column={}&output_file={}&class_column={}&n_row={}' \
                                .format(self.input_file, self.separator, self.columns_to_show,
                                        self.help_column, self.output_file, self.class_column, 1))
        self.assertNotEqual(response.status_code, 404)
        self.assertTrue(os.path.exists('output_test_partial.csv'))
        df = pd.read_csv('output_test_partial.csv', sep=';', encoding='utf-8')
        self.assertEqual(df.shape[0], 1)
