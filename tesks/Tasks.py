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
import sqlalchemy
from sqlalchemy import create_engine

class RedditTaskManager():
    tasks = []
    current_task = AbstractRedditTask
    reddit_conn = praw.Reddit

    def __init__(self, bot_name, tasks):
        for task in tasks:
            self.add_task(task)
        self.reddit_conn = praw.Reddit(bot_name)

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
                message for message in self.reddit_conn.get_unread(limit=None)
                if message.subject == self.current_task.trigger
            ]

    def run_task(self):
            pass

    def run(self):
        for task in self.tasks:
            self.current_task = task
            messages = self.match_messages()
            for message in messages:
                if self.current_task.handle(message):
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