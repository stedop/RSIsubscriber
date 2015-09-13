#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from rsisubscribers.Reddit import RSIsubscribers
from datetime import datetime
import time
import logging

LOGFORMAT = '%(asctime)-15s %(message)s'


def main():
    """
    main commands
    :return:
    """

    """ init log """
    logging.basicConfig(
        filename = "subscriber_bot.log",
        filemode="w",
        level = logging.WARN,
        format=LOGFORMAT
    )

    error_count = 0
    while True:
        try:
            rsi_subscribers = RSIsubscribers('dopscsstesting')
            rsi_subscribers.connect()
            sbuscriber_messages = rsi_subscribers.get_messages('Subscriber')
            if sbuscriber_messages:
                rsi_subscribers.check_subscriptions(sbuscriber_messages)
            """ Todo check messages for subject change flair to allow big users to pick subscriber or monocle """
        except Exception as error:
            logging.exception(error)
            error_count += 1
            if error_count < 5:
                pass
            else:
                logging.error("5 Errors in a row, shutting down")
                raise
    time.sleep(3 * 60)


main()