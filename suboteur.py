#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import logging
import datetime
from Bot import BNBot
from Bot import TaskManager
from Bot import MessageNotFoundException
from Tasks.r_rsisubscribers import CheckSubscriberMessagesTask
from Tasks.r_rsisubscribers import AuthenticateSubscribersTask
from Tasks.r_rsisubscribers import UpdateFlairTask
from Tasks.r_rsisubscribers import UpdateDBTask
import os

""" Base directory setup """
BASEDIR = os.path.dirname(os.path.realpath(__file__)) + "/"

""" dev Contact """
dev = 'dops <dopstephen@gmail.com>'

""" init log """
today = datetime.date.today()
logfile = BASEDIR + "/Logs/Suboteur/" + today.strftime('%d-%b-%Y') + ".log"

LOGFORMAT = '\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
DATEFORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    filename=logfile,
    filemode="a",
    level=logging.WARNING,
    format=LOGFORMAT,
    datefmt=DATEFORMAT
)
logging.captureWarnings(True)
bot_logger = logging.getLogger('TheBot')

""" Config File """
config_file = 'rsi_config.ini'

""" Main """
try:
    """ Tasks """
    tasks = [CheckSubscriberMessagesTask, AuthenticateSubscribersTask, UpdateFlairTask, UpdateDBTask]
    bot = BNBot(BASEDIR, config_file, bot_logger)
    task_manager = TaskManager(tasks, bot)
    task_manager.run()

except MessageNotFoundException as message_not_found:
    bot_logger.exception(message_not_found)
    # Todo send message to mods and continue operations
    pass

except Exception as error:
    # Todo on a fatal error send message to bot owner and dev
    bot_logger.exception(error)
    pass