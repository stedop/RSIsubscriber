#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import logging
import datetime
from Bot.TheBot import Bot
from Bot.TasksManager import TaskManager
from Tasks.r_rsisubscribers.MessageTestTasks import SendMessageTask
from Bot.Exceptions import MessageNotFoundException

""" init log """
today = datetime.date.today()
logfile = "Logs/" + today.strftime('%d-%b-%Y') + ".log"

LOGFORMAT = '\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
DATEFORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    filename=logfile,
    filemode="a",
    level=logging.WARN,
    format=LOGFORMAT,
    datefmt=DATEFORMAT
)
logging.captureWarnings(True)
bot_logger = logging.getLogger('TheBot')

""" Main """
try:
    tasks = [SendMessageTask]
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