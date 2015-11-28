#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import logging
import datetime
from Bot.TheBot import Bot
from Bot.TasksManager import TaskManager
from Tasks.r_rsisubscribers.SubscriberTasks import CheckSubscriberMessagesTask, AuthenticateSubscribersTask
from Bot.Exceptions import MessageNotFoundException

""" init log """
LOGFORMAT = '%(asctime)-15s %(message)s \n\n'
today = datetime.date.today()
logfile = "Logs/" + today.strftime('%d-%b-%Y') + ".log"
logging.basicConfig(
    filename=logfile,
    filemode="a+",
    level=logging.WARN,
    format=LOGFORMAT
)
logging.captureWarnings(True)
bot_logger = logging.getLogger('TheBot')

try:
    tasks = [CheckSubscriberMessagesTask, AuthenticateSubscribersTask]
    myBot = Bot('rsi_config.ini', bot_logger)

    task_manager = TaskManager(tasks, myBot)
    task_manager.run()

except MessageNotFoundException as message_not_found:
    bot_logger.exception(message_not_found)
    # Todo send message to mods and continue operations
    pass
except Exception as error:
    # Todo on a fatal error send message to bot owner and dev
    bot_logger.exception(error)
    pass
