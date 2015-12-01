#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Message Test tasks
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""

from Bot import AbstractTaskType
from DataModels import MessagesModel

class SendMessageTask(AbstractTaskType):
    """
    Simple sends every message to u/dops for check
    """

    def requirements(self):
        return True

    def handle(self, requirements):
        messages = self.bot.data_manager.query(MessagesModel).all()

        for message in messages:
            self.bot.logger.debug(message.name)
            self.bot.send_message(message.name, 'dops', subscriber_name="MrChance", max_backer_status="Commander")
