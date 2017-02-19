# -*- coding: utf-8 -*-
"""App Definition for SwitchyWitchy"""

import curio

from .config import app_confs
from .models import Trap


class SwitchyWitchy(object):
    """The application obj."""

    def __init__(self):
        self.watches = []
        self.queue = curio.Queue()

    def setup_watches(self):
        """
        Setup the app watches based on the configurations.
        """
        apps = app_confs()
        for app in apps.sections():
            app_property = apps[app]
            self.watches.append(Trap(app_property, self.queue))
