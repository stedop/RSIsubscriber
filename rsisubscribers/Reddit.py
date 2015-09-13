#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
RSIsubscribers
~~~~~~~~~~~~~~~
Class to be used when accessing reddit and processing messages
:license: MIT
"""
import praw
from rsisubscribers.Subscribers import Subscribers
from rsisubscribers.DataManager import Subscriber, Flair
from twistar.registry import Registry

""" Need to abstract this away to a config manager """
DB_USER = ""
DB_PASS = ""
DB_NAME = "rsi_subscribers"

Registry.DBPOOL = adbapi.ConnectionPool('MySQLdb', user=DB_USER, passwd=DB_PASS, db=DB_NAME)
Date = Registry.getDBAPIClass("Date")

class RSIsubscribers:
    r = []
    data_manager = []

    def __init__(self, subreddit_name):
        """
            Initialise
            :param subreddit_name:
            :return:
        """
        self.r = praw.Reddit('RSIsubscribers test')
        self.subreddit_name = subreddit_name
        self.subscriber_flair = []
        self.data_manager = DataManager()

    def connect(self):
        """
            Connect to reddit, uses OAuth settings in praw.ini
            :return bool
        """
        if self.r.refresh_access_information():
            return True
        else:
            raise RuntimeError

    def get_messages(self, subject):
        """
            Gets all unread messages in inbox where the subject is Subscriber
            :return praw.Messages
        """
        return [message for message in self.r.get_unread(limit=None) if message.subject == subject]

    def check_subscriptions(self, messages):
        """
            Checks the username provided in the message body against the RSI api and performs actions
            :param messages: list
        """

        """ Get the two basic flairs from db """
        self.subscriber_flair = FlairChoice(
            Flair().find(1),
            Flair().find(2)
        )

        for message in messages:
            subscribers = Subscribers()
            is_subscriber = subscribers.is_subscriber(message.body)
            self.update_flair(message.author, self.subscriber_flair, is_subscriber)

            """ todo THIS NEEDS WORK """
            subscriber = Subscriber.findBy(where=['reddit_username=' + message.author], limit=1)
            print(subscriber)
            if not subscriber:
                subscriber = Subscriber()

            subscriber.reddit_username = message.author
            subscriber.rsi_username = message.body
            subscriber.is_monocle = 0
            subscriber.months = 1
            subscriber.addRelation(self.subscriber_flair.get_flair(is_subscriber))
            print(subscriber)
            subscriber.save()

            message.mark_as_read()

    def update_flair(self, username, flair_object, condition=False):
        """
            Updates the flair of the given user, depending on condition
            :param username: string
            :param condition: bool
            :param flair_object: FlairChoice
        """
        self.r.get_subreddit(
            self.subreddit_name).set_flair(
            username,
            flair_object.get_text(condition),
            flair_object.get_class(condition)
        )


class FlairChoice:

    def __init__(self, true_flair, false_flair):
        """
            Initialise
            :param true_flair Flair:
            :param false_flair Flair:
            :return:
        """
        self.true_flair = true_flair
        self.false_flair = false_flair

    def get_flair(self, condition):
        """
            Gets the flair based on condition
            :param condition:
            :return Flair:
        """
        if (condition):
            return self.true_flair
        else:
            return self.false_flair

    def get_text(self, condition):
        """
            Get the flair message based on condition
            :param condition:
            :return string:
        """
        flair = self.get_class(condition)
        return flair.text

    def get_class(self, condition):
        """
            Get the flair class based on condition
            :param condition:
            :return string:
        """
        flair = self.get_class(condition)
        return flair.css_class