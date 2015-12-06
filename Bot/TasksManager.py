#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
Tasks management and definition
:license: MIT
"""

from abc import ABCMeta, abstractmethod
from Bot.TheBot import BNBot


class TaskManager(object):
    """
    Task management service
    """

    tasks = []
    __current_task = []

    def __init__(self, tasks, bot=BNBot):
        """

        :param tasks:
        :param bot:
        :return:
        """
        for task in tasks:
            self.add_task(task(bot))

    def add_task(self, task):
        """
        Add task to task list

        :param task:
        :return:
        """
        self.tasks.append(task)

    def run_task(self, task):
        """
        Run the task

        :param task:
        :return:
        """
        requirements = task.requirements()
        if requirements:
            return task.handle(requirements)

        return False

    def run(self):
        if self.tasks:
            for task in self.tasks:
                self.run_task(task)


class AbstractTaskType(object):
    """
    Task Definition
    """
    __metaclass__ = ABCMeta
    bot = None

    def __init__(self, bot=BNBot):
        """
        Sets the bot and gets the mod list

        :param bot:
        :return:
        """
        self.bot = bot

    @abstractmethod
    def handle(self, *requirements):
        """
        Business logic of the task

        :param requirements:
        :return:
        """
        return True

    @abstractmethod
    def requirements(self):
        """
        Handles the trigger, if it returns requirements then pass them to the handle

        :return bool:
        """
        requirements = []
        return requirements
