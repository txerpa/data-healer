# -*- coding: utf-8 -*-

"""Views configs"""

import os
import json
import unittest

import pandas as pd

from healer.app import create_app
from healer.settings import TestConfig
import conf


class ViewTests(unittest.TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        self.app = app.test_client()

        self.df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.df.to_csv('data/input_test.csv', sep=';', encoding='utf-8')

        conf.CSV_SEPARATOR = ';'
        conf.INPUT_FILE = 'data/input_test.csv'
        conf.COLUMNS_TO_SHOW = ['col1', ]
        conf.HELP_COLUMN = None
        conf.CATEGORIES = ['A', 'B', 'C']
        conf.OUTPUT_FILE = 'data/output_test.csv'

    def tearDown(self):
        os.remove('data/input_test.csv')
        # os.remove('data/output_test.csv')

    def test_home(self):
        response = self.app.get('/')
        self.assertNotEqual(response.status_code, 404)

    def test_about(self):
        response = self.app.get('/about/')
        self.assertNotEqual(response.status_code, 404)

    def test_get_row(self):
        response = self.app.get('/get_row?n_row=0')
        self.assertNotEqual(response.status_code, 404)

    def test_get_categories(self):
        response = self.app.get('/get_categories/')
        self.assertNotEqual(response.status_code, 404)

    def test_post_row(self):
        response = self.app.post('/post_row/',
                                 data=json.dumps({'n_row': 0, 'category': 'A'}), content_type='application/json')
        self.assertNotEqual(response.status_code, 404)
