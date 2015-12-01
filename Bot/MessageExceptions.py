#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Exceptions for the bot
~~~~~~~~~~~~~~~
:license: MIT
:author: Stephen Dop
"""


class MessageNotFoundException(Exception):
    """
    If a template message isn't found
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
