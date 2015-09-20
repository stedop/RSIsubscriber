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
    filemode="w",
    level=logging.WARN,
    format=LOGFORMAT
)
logging.captureWarnings(True)

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
    raise
