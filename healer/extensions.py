# -*- coding: utf-8 -*-

"""
Extensions module. Each extension is initialized in the app factory located in app.py.
"""

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect

bcrypt = Bcrypt()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
webpack = Webpack()
