#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
Reddit Connection Management
Is setup to handle multi threading
:license: MIT
"""

import praw

class Connection:
    __reddit_conn = praw.Reddit

    def __init__(self, app_name):
        self.__reddit_conn = praw.Reddit(app_name)
