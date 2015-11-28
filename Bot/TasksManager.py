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
from mako.template import Template
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
        """
        Sets the bot and gets the mod list
        :param bot:
        :return:
        """
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
        """
        Matches any unread messages with the subject variable and returns then as a dict
        :param subject:
        :return:
        """
        messages = self.bot.reddit.get_unread([message for message in self.bot.reddit.get_unread(limit=None) if message.subject == subject])
        return messages

    def send_message(self, template_name=None, user_name=None, **template_values):
        """
        Sends message to the user from the templates db
        :param template_name:
        :param user_name:
        :param template_values:
        :return:
        """
        if template_name:
            template_body = self.bot.data_manager.query(
                            MessagesModel
                        ).filter(
                            MessagesModel.name == template_name
                        ).first()
            if template_body:
                template_values.update(user_name=user_name)
                body = Template(template_body).render(template_values)
                self.bot.reddit.send_message(user_name, template_body.subject, body)
            else:
                raise MessageNotFoundException("Message with the name " + template_name + " not found")
                pass
        return True

    def set_flair(self, user_name, flair_id):
        """
        Sets a users flair based on a db entry
        Also why do I keep spelling flair "fliar"
        :param user_name:
        :param flair_id:
        :return:
        """
        flair = self.bot.data_manager.query(FlairModel).get(flair_id)
        if flair:
            self.bot.reddit.set_flair(self.bot.config.get("reddit.subreddit"), user_name, flair.text, flair.css_class)
            return flair

        return False

    def is_mod(self, user_name):
        """
        Checks to see if a user is a mod of the config subreddit
        :param user_name:
        :return:
        """
        if user_name in self.mod_list:
            return True

        return False