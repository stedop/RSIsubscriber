#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
Tasks management and definition
:license: MIT
"""

from abc import ABCMeta, abstractmethod
from DataModels.MessagesModel import MessagesModel
from DataModels.FlairModel import FlairModel
from Bot.Exceptions import MessageNotFoundException
from Bot.TheBot import Bot
import re

class TaskManager():
    """
    Task management service
    """

    tasks = []
    __current_task = []

    def __init__(self, tasks, bot=Bot):
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
    mod_list = []

    def __init__(self, bot=Bot):
        self.bot = bot
        for mod in bot.reddit.get_subreddit(bot.config.get("reddit.subreddit")).get_moderators():
            self.mod_list.append(mod.name)

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

    def match_unread(self, subject):
        messages = self.bot.reddit.get_unread([message for message in self.bot.reddit.get_unread(limit=None) if message.subject == 'Subscriber'])
        return messages

    def send_message(self, template_name=None, user_name=None, **replacements):
        if (template_name):
            template = self.bot.data_manager.query(
                            MessagesModel
                        ).filter(
                            MessagesModel.name == template_name
                        ).first()
            if template:
                body = re.sub("|| username ||", user_name, template.body)
                for key, value in replacements:
                    body = re.sub("|| " + key + "||", value, body)

                self.bot.reddit.send_message(user_name, template.subject, body)
            else:
                # Todo uncomment below add username to information so the mods know who to contact
                # raise MessageNotFoundException("Message with the name " + template_name + " not found")
                pass
        return True

    def set_flair(self, user_name, flair_id):
        flair = self.bot.data_manager.query(FlairModel).get(flair_id)
        if flair:
            self.bot.reddit.set_flair(user_name, flair.text, flair.css_class)
            return flair

        return False

    def is_mod(self, user_name):
        if user_name in self.mod_list:
            return True

        return False