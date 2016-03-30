#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import logging
import datetime
from Bot.TheBot import BNBot
from Bot.TasksManager import TaskManager
from Tasks.r_starcitizen_trades.PrivateMessageTask import ConfirmCitizenTask, RemoveFlairTask
from Tasks.r_starcitizen_trades.WikiTask import RemovedFlairWikiTask
import os


BASEDIR = os.path.dirname(os.path.realpath(__file__)) + "/"

""" init log """
today = datetime.date.today()
logfile = BASEDIR + "/Logs/flairbot/" + today.strftime('%d-%b-%Y') + ".log"

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
bot_logger = logging.getLogger('Flairbot')

""" Main """
try:
    tasks = [ConfirmCitizenTask, RemoveFlairTask, RemovedFlairWikiTask]
    bot = BNBot(BASEDIR, 'flairbot_config.ini', bot_logger)
    task_manager = TaskManager(tasks, bot)
    task_manager.run()

except Exception as error:
    # Todo on a fatal error send message to bot owner and dev
    bot_logger.exception(error)
    pass
