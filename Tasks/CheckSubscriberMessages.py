#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""

from src.TasksManager import AbstractTaskType
from DataModels.SubScriberModel import SubscriberModel

class CheckSubscriberMessagesTest(AbstractTaskType):
    def handle(self, requirements):
        """
        Handle the messages
        :return:
        """
        messages = requirements['messages']
        subscribers_api = (requirements['subscribers'])
        for message in messages:
            if subscribers_api.is_subscriber(messages.author):
                pass

    def requirements(self):
        """
        Get Subscriber Messages
        :return:
        """
        sbuscriber_messages = self.bot.r.get_unread([message for message in self.bot.r.get_unread(limit=None) if message.subject == 'Subscriber'])
        if sbuscriber_messages:
            return {'messages': sbuscriber_messages, 'subscribers': SubscribersAPI()}
        return False