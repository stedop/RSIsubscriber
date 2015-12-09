#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# encoding=utf8


import sys
import logging
import datetime
from Bot.TheBot import BNBot
from Bot.TasksManager import TaskManager
from Tasks.r_rsisubscribers.MessageTestTasks import SendMessageTask
from Bot.MessageExceptions import MessageNotFoundException
import os

reload(sys)
sys.setdefaultencoding('utf8')
BASEDIR = os.path.dirname(os.path.realpath(__file__)) + "/"

""" init log """
today = datetime.date.today()
logfile = BASEDIR + "Logs/" + today.strftime('%d-%b-%Y') + "_test.log"

LOGFORMAT = '\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
DATEFORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    filename=logfile,
    filemode="a",
    level=logging.DEBUG,
    format=LOGFORMAT,
    datefmt=DATEFORMAT
)
logging.captureWarnings(True)
bot_logger = logging.getLogger('TheBot')
bot_logger.debug(sys.getdefaultencoding());
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
""" Main """
try:
    tasks = [SendMessageTask]
    # test_bot = BNBot(BASEDIR, 'rsi_config.ini', bot_logger)
    # task_manager = TaskManager(tasks, test_bot)
    # task_manager.run()

except MessageNotFoundException as message_not_found:
    bot_logger.exception(message_not_found)
    # Todo send message to mods and continue operations
    pass

except Exception as error:
    # Todo on a fatal error send message to bot owner and dev
    bot_logger.exception(error)
    pass