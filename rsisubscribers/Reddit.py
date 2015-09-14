#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
RSIsubscribers
~~~~~~~~~~~~~~~
Class to be used when accessing reddit and processing messages
:license: MIT
"""
import praw
from rsisubscribers.SubscribersAPI import SubscribersAPI
from rsisubscribers.DataManager import SubscriberModel, FlairModel, MessagesModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

""" Todo Need to abstract this away to a config manager """
DB_USER = "root"
DB_PASS = "rawjj3i"
DB_HOST = "127.0.0.1"
DB_NAME = "rsi_subscribers"

Session = sessionmaker()


class RSIsubscribers:
    r = []
    data_manager = []

    def __init__(self, subreddit_name, dsn="mysql+mysqldb://{}:{}@{}/{}".format(DB_USER, DB_PASS, DB_HOST, DB_NAME)):
        """
            Initialise
            :param subreddit_name:
            :return:
        """
        self.r = praw.Reddit('RSIsubscribers test')
        self.subreddit_name = subreddit_name
        self.db_engine = create_engine(dsn)
        self.db_session = Session(bind=self.db_engine)

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
        api = SubscribersAPI()

        """ Get the two basic flairs from db """
        subscriber_flair = FlairChoice(
            self.db_session.query(FlairModel).get(1),
            self.db_session.query(FlairModel).get(2)
        )

        for message in messages:
            is_subscriber = api.is_subscriber(message.body)
            is_high_rank = api.is_high_rank(message.body)

            self.update_flair(message.author, subscriber_flair, is_subscriber)

            subscriber = self.db_session.query(SubscriberModel).filter(SubscriberModel.reddit_username == message.author).first()

            if not subscriber:
                subscriber = SubscriberModel()

            subscriber.reddit_username = message.author
            subscriber.rsi_username = message.body
            subscriber.is_monocle = 0
            subscriber.current = 1 if is_subscriber else 0
            subscriber.flair = subscriber_flair.get_flair(is_subscriber)

            if is_high_rank:
                self.send_message(
                    message.author,
                    self.db_session.query(MessagesModel).filter(MessagesModel.name == "flair_choice")
                )

            self.db_session.add(subscriber)
            self.db_session.commit()
            message.mark_as_read()

    def update_all_records(self):
        api = SubscribersAPI()
        thinking_fliar = self.db_session.query(FlairModel).get(1)

        for subscriber in self.db_session.query(SubscriberModel).filter(SubscriberModel.current == 1):
            is_subscriber = api.is_subscriber(subscriber.rsi_username)
            if is_subscriber:
                subscriber.months =+ 1
                if subscriber.months >= 12:
                    self.send_message(
                        subscriber.reddit_username,
                        self.db_session.query(MessagesModel).filter(MessagesModel.name == "flair_choice")
                    )
            else:
                subscriber.current = 0
                subscriber.flair = thinking_fliar

    def handle_flair_choice(self, messages):
        """ Get the two basic flairs from db """
        choice_flair = FlairChoice(
            self.db_session.query(FlairModel).get(2),
            self.db_session.query(FlairModel).get(3)
        )

        api = SubscribersAPI()

        for message in messages:
            is_subscriber = api.is_subscriber(message.body)
            if is_subscriber:
                if message.body == "Subscriber":
                    self.update_flair(message.author, choice_flair, True)
                elif message.body == "Monocle":
                    self.update_flair(message.author, choice_flair, False)
                else:
                    self.send_message(
                        message.author,
                        self.db_session.query(
                            MessagesModel
                        ).filter(
                            MessagesModel.name == "flair_choice_not_allowed"
                        )
                    )
            else:
                self.send_message(
                        message.author,
                        self.db_session.query(
                            MessagesModel).
                            filter(
                                MessagesModel.name == "not_found_in_api"
                            )
                    )
        pass

    def send_message(self, reddit_username, message=MessagesModel):
        """
        Sends a message to a user that informs them of special flair
        :param reddit_username:
        :param message Messages:
        :return:
        """
        self.r.send_message(reddit_username, message.subject, message.body)
        return True

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
            :param true_flair FlairModel:
            :param false_flair FlairModel:
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
        flair = self.get_flair(condition)
        return flair.text

    def get_class(self, condition):
        """
            Get the flair class based on condition
            :param condition:
            :return string:
        """
        flair = self.get_flair(condition)
        return flair.css_class