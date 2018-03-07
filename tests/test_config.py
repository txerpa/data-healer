# -*- coding: utf-8 -*-

"""Test configs"""

from healer.app import create_app
from healer.settings import ProdConfig, DevConfig, TestConfig


def test_production_config():
    """Production config"""
    app = create_app(ProdConfig)
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False
    assert app.config['DEBUG_TB_ENABLED'] is False


def test_dev_config():
    """Development config"""
    app = create_app(DevConfig)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True


def test_test_config():
    """Test config"""
    app = create_app(TestConfig)
    assert app.config['ENV'] == 'test'
    assert app.config['DEBUG'] is True
