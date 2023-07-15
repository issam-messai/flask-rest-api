"""
Default conf file for the app
To overide it set your custom conf.py via env var MYAPP_CONF_FILE
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
