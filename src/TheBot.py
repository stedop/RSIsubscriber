#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
TheBot
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""
from src.TasksManager import TaskManager
from src.ConfigManager import ConfigManager
from src.DataManager import DataManager
from praw.handlers import MultiprocessHandler
import praw
import atexit

class Bot:
    config = ConfigManager
    __tesk_manager = TaskManager
    data_manager = DataManager
    r = praw.Reddit

    def __init__(self, config_file, tasks=None):
        self.config = ConfigManager(config_file)

        if self.config.section_exists('database'):
            self.data_manager = DataManager(
                self.config.get('database.user'),
                self.config.get('database.pass'),
                self.config.get('database.host'),
                self.config.get('database.name')
            )

        user_agent = (self.config.get("reddit.bot_name"))
        handle = MultiprocessHandler()

        self.r = praw.Reddit(
            user_agent=user_agent,
            log_requests=self.config.get('reddit.log_requests'),
            handle=handle,
            config_file=self.config.get('reddit.config_file')
        )

        if not self.r.refresh_access_information():
            raise RuntimeError
        # atexit.register(self.close_conns, self.r, self.data_manager)
        self.__tesk_manager = TaskManager(tasks, self)
        self.__tesk_manager.run()
