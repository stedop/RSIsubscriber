#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from rsisubscribers.Reddit import RSIsubscribers
from datetime import datetime
import time
import logging

LOGFORMAT = '%(asctime)-15s %(message)s'

"""
    TODO    This could potentially be turned into a an app class which acts as a wrapper
            for all uses of the bot.  Essentially each class is a service which implements
            an interface, allowing for the extension.  This is much more SOLID

            We can also add actions via an api catcher, This would allow for routing which
            can then be linked to buttons on a subreddit, in theory you could build some
            very interesting mod tools.

            One could setup a website which allows any subreddit to create a username and login
            amd allow the app to access the currently logged in reddit account (the bot account)
            which automatically sets up the bot to that account and  will let you generate the
            code for buttons.  You could even build a little admin to allow them to setup
            catches and actions and even a interface that allows you to add your own extension
            from github

            Error handling can be done by overridden exceptions using sys.excepthook
            Logging can be done using the setHandler method
            Watch this space!!!
"""

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