#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import logging
import datetime

from Bot.TheBot import Bot
from Bot.TasksManager import TaskManager
from Tasks.r_rsisubscribers.SubscriberTasks import CheckSubscriberMessagesTask, AuthenticateSubscribersTask


error_count = 0

try :
    tasks = [CheckSubscriberMessagesTask, AuthenticateSubscribersTask]
    myBot = Bot('rsi_config.ini')
    task_manager = TaskManager(tasks, myBot)
    task_manager.run()

except Exception as error:
    logging.exception(error)
    error_count += 1
    raise
