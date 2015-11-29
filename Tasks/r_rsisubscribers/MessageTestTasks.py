#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Message Test tasks
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""

from Bot.TasksManager import AbstractTaskType
from DataModels.MessagesModel import MessagesModel
from DataModels.SubscriberModel import SubscriberModel
from DataModels.FlairModel import FlairModel


class SendMessageTask(AbstractTaskType):
    """
    Simple sends every message to u/dops for check
    """

    def requirements(self):
        return True

    def handle(self, requirements):
        messages = self.bot.data_manager.query(MessagesModel).all()
        self.bot.logger.debug("All messages")
        self.bot.logger.debug(messages)

        for message in messages:
            self.bot.logger.debug("Message")
            self.bot.logger.debug(message)
            self.send_message(message.name, 'dops')