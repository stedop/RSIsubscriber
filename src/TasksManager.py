#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
Tasks management and definition
:license: MIT
"""

from abc import ABCMeta, abstractmethod, abstractstaticmethod



class TaskManager():
    """
    Task management service
    """

    tasks = []
    __current_task = []

    def __init__(self, tasks, bot):
        """

        :param tasks:
        :param bot Bot:
        :return:
        """
        for task in tasks:
            self.add_task(task(bot))


    def add_task(self, task):
        """
        Add task to task list
        :param task AbstractRedditTask:
        :return:
        """
        self.tasks.append(task)

    def run_task(self, task):
        """
        Run the task
        :param task AbstractTaskType:
        :return:
        """
        requirements = task.requirements()
        if requirements:
            return task.handle(requirements)

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

    def __init__(self, bot):
        self.bot = bot

    @abstractmethod
    def handle(self, requirements):
        """
        Busienss logic of the task
        :return bool:
        """
        return True

    @abstractmethod
    def requirements(self):
        """
        Handles the trigger, if it returns requierments then pass them to the handle
        :return bool:
        """
        requirements = []
        return requirements