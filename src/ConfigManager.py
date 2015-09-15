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
        self.parser.sections()
        print(self.config['DB']['host'])

    def get(self, keyname):
        for step in keyname.split("."):
            pass

    def set(self, keyname, value):
        for step in keyname.split("."):
            pass

    def __del__(self):
        """with open(self.config_filename, 'w') as configfile:
            self.parser.write(configfile)"""