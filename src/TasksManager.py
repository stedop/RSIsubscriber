#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
Tasks managment and definition
:license: MIT
"""

from abc import ABCMeta, abstractmethod

import praw
from sqlalchemy import create_engine
from sqlalchemy.orm import session

from src import ConfigManager


class RedditTaskManager():
    tasks = []
    __current_task = {}
    __reddit_conn = praw.Reddit
    __db_session = session
    __db_engine = create_engine
    __config = ConfigManager

    def __init__(self, config, tasks=[]):
        self.__config = config

        self.__reddit_conn = praw.Reddit(self.__config.get("DEFAULT.bot_name"))
        dsn_list = [
            self.__config.get("DB.user"),
            self.__config.get("DB.pass"),
            self.__config.get("DB.host"),
            self.__config.get("DB.name"),
        ]
        self.__db_engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(dsn_list)
        )

        for task in tasks:
            self.add_task(task)

    def add_task(self, task):
        """
        Add task to task list
        :param task AbbstractRedditTask:
        :return:
        """
        self.tasks.append(task.trigger)

    def match_messages(self):
        """
        Match any unread messages to task
        :return:
        """
        return \
            [
                message for message in self.__reddit_conn.get_unread(limit=None)
                if message.subject == self.__current_task.trigger
            ]

    def run_task(self):
            pass

    def run(self):
        for task in self.tasks:
            self.__current_task = task
            messages = self.match_messages()
            for message in messages:
                if self.__current_task.handle(message):
                    message.mark_as_read()


class AbstractRedditTask(object):
    __metaclass__ = ABCMeta

    trigger = ""
    db = False

    def __init__(self, trigger, dsn=False):
        self.trigger = trigger
        if dsn:
            self.db = create_engine(dsn)

    @abstractmethod
    def handle(self):
        pass