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
import datetime


class SendMessageTask(AbstractTaskType):
    """
    Simple sends every message to u/dops for check
    """

    def requirements(self):
        return True;

    def handle(self, requirements):
        messages = MessagesModel.query.all()

        for message in messages:
            self.send_message(messages.name,'dops');
