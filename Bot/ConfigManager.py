#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
Config management and definition
:license: MIT
"""

import configparser
import atexit


def cleanup(parser, config_filename):
        with open(config_filename, 'w') as configfile:
            parser.write(configfile)

class ConfigManager:
    parser = configparser.ConfigParser
    config_filename = ""
    config = []

    def __init__(self, config_filename):
        """
        Parses and reads the config file, sets up the write when the program is complete
        :param config_filename:
        :return:
        """
        self.config_filename = config_filename.decode('utf8')
        self.parser = configparser.ConfigParser()
        self.parser.BOOLEAN_STATES = {'1': True, '0': False}
        self.config = self.parser.read(self.config_filename)
        atexit.register(cleanup, self.parser, self.config_filename)

    def get(self, keyname):
        """
        Gets a config value using dot notation
        e.g. "reddit.subreddit"
        :param keyname:
        :return:
        """
        steps = keyname.split('.')
        if len(steps) == 1:
            return  self.parser.get(steps[0], fallback=False)

        return self.parser.get(steps[0], steps[1], fallback=False)

    def set(self, keyname, value=""):
        """
        Sets a config value or section
        :param keyname:
        :param value:
        :return:
        """
        steps = keyname.split('.')
        if len(steps) == 1:
            self.parser.add_section(steps[0])
            return True

        if not self.parser.has_section(steps[0]):
            self.parser.add_section(steps[0])

        if self.parser.set(steps[0], steps[1], value):
            return True

        return False

    def section_exists(self, section):
        """
        Checks to see if that section exists
        :param section:
        :return:
        """
        return self.parser.has_section(section)