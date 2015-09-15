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
        filename="subscriber_bot.log",
        filemode="w",
        level=logging.WARN,
        format=LOGFORMAT
    )
    logging.captureWarnings(True)

    error_count = 0

    rsi_subscribers = RSIsubscribers('RSIsubscribertesting')
    rsi_subscribers.connect()
    while True:
        try:
            """ Handle subscriber messages """
            sbuscriber_messages = rsi_subscribers.get_messages('Subscriber')
            if sbuscriber_messages:
                rsi_subscribers.check_subscriptions(sbuscriber_messages)

            """ Handle flair choice messages """
            monocle_messages = rsi_subscribers.get_messages('Select Flair')
            if monocle_messages:
                rsi_subscribers.handle_flair_choice(monocle_messages)

            # if datetime.today().day == 15:
                # rsi_subscribers.update_all_records()
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