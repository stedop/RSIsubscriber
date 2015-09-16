#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
Config management and definition
:license: MIT
"""

import configparser


class ConfigManager:
    parser = configparser.ConfigParser
    config_filename = ""
    config = []

    def __init__(self, config_filename):
        self.config_filename = config_filename
        self.parser = configparser.ConfigParser()
        self.parser.BOOLEAN_STATES = {'1': True, '0': False}
        self.config = self.parser.read(self.config_filename)

    def get(self, keyname):
        steps = keyname.split('.')
        return self.parser.get(steps[0], steps[1],fallback=False)

    def set(self, keyname, value=""):
        steps = keyname.split('.')
        if len(steps) == 1:
            self.parser.add_section(steps[0])
            return True

        if not self.parser.has_section(steps[0]):
            self.parser.add_section(steps[0])

        if self.parser.set(steps[0], steps[1], value):
            return True

        return False

    def __del__(self):
        with open(self.config_filename, 'w') as configfile:
            self.parser.write(configfile)