#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import logging
import datetime

from Bot.TheBot import Bot
from Tasks.r_rsisubscribers.SubscriberTasks import CheckSubscriberMessagesTask, AuthenticateSubscribersTask


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

error_count = 0

try :
    tasks = [CheckSubscriberMessagesTask, AuthenticateSubscribersTask]
    myBot = Bot('rsi_config.ini', tasks)
except Exception as error:
    logging.exception(error)
    error_count += 1
    raise
