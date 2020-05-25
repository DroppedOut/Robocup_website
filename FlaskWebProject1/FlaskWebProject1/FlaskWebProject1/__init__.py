"""
The flask applicationlication package.
"""

from flask import Flask

application = Flask(__name__)

import Robocup.views
