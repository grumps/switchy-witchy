# -*- coding: utf-8 -*-
"""SwitchyWitchy App"""
__author__ = 'Maxwell J. Resnick'
__email__ = 'max@ofmax.li'
__version__ = '0.1.0'

import logging

from .switchywitchy import SwitchyWitchy
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename="debug.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)
