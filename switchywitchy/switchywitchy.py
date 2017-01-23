# -*- coding: utf-8 -*-
"""App Definition for SwitchyWitchy"""

from .config import app_confs
from .models import Trap


class SwitchyWitchy(object):
    """The application obj."""

    def __init__(self):
        self.watches = []

    def setup_watches(self):
        """
        Setup the app watches based on the configurations.
        """
        apps = app_confs()
        for app in apps.sections():
            app_property = apps[app]
            self.watches.append(Trap(app_property))
