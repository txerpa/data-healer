# -*- coding: utf-8 -*-

"""
Extensions module. Each extension is initialized in the app factory located in app.py.
"""

from flask.helpers import get_debug_flag
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_webpack import Webpack

bcrypt = Bcrypt()
cache = Cache()
webpack = Webpack()

if get_debug_flag():
    from flask_debugtoolbar import DebugToolbarExtension
    debug_toolbar = DebugToolbarExtension()
