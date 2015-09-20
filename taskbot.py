#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import logging
from Bot.TheBot import Bot
from Bot.TasksManager import TaskManager
from Tasks.r_rsisubscribers.SubscriberTasks import CheckSubscriberMessagesTask, AuthenticateSubscribersTask
from Bot.Exceptions import MessageNotFoundException
error_count = 0

try:
    tasks = [CheckSubscriberMessagesTask, AuthenticateSubscribersTask]
    myBot = Bot('rsi_config.ini')

    task_manager = TaskManager(tasks, myBot)
    task_manager.run()

except MessageNotFoundException as message_not_found:
    logging.exception(message_not_found)
    # Todo send message to mods and continue operations
    pass
except Exception as error:
    # Todo on a fatal error send message to bot owner and dev
    logging.exception(error)
    error_count += 1
    raise
