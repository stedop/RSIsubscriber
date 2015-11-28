#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Subscription tasks
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""

from Bot.TasksManager import AbstractTaskType
from DataModels.CitizensAPI import CitizensAPI
from DataModels.SubscriberModel import SubscriberModel
from DataModels.FlairModel import FlairModel
from Bot.Exceptions import CitizenNotFoundException
import datetime


class CheckSubscriberMessagesTask(AbstractTaskType):
    """
    Checks for messages with "Subscriber" and handles the result
    ~~~~~~~~~~~~~~~
    MCP
    :license: MIT
    :messages used: 'citizen_not_found',
                    'subscription_auth',
                    'subscription_not_auth',
                    'no_subscription_auth',
                    'no_subscription_no_auth'
    """
    citizens_api = CitizensAPI()

    def handle(self, requirements):
        """
        Handle the messages

        :param requirements:
        :return:
        """
        messages = requirements['messages']
        for message in messages:
            try:
                is_subscribing = self.citizens_api.is_subscribing(message.body)
            except CitizenNotFoundException as not_found:
                self.send_message('citizen_not_found', message.author)
                self.bot.logger.exception(not_found)
                continue

            flair_id = 2
            if is_subscribing is True:
                self.subscribing(message, flair_id)
            else:
                self.not_subscribing(message, flair_id)
            message.mark_as_read()

        # Commits DB changes
        self.bot.data_manager.commit()
        return True

    def requirements(self):
        """
        Get Subscriber Messages
        :return:
        """
        subscriber_messages = self.match_unread('Citizen')
        if subscriber_messages:
            return {'messages': subscriber_messages}
        return False

    def subscribing(self, message, flair_id):
        is_subscribing = True
        is_authenticated = self.citizens_api.is_authenticated(message.body)
        highest_rank = self.citizens_api.get_rank(message.body)

        if is_authenticated:
            flair_id = 1
            self.send_message('subscription_auth', message.author)
        else:
            self.send_message('subscription_not_auth', message.author)

        flair = self.set_flair(message.author, flair_id)
        current = True
        self.update_subscriber_database(
            message.author,
            message.body,
            current,
            highest_rank,
            is_subscribing,
            is_authenticated,
            flair
        )

    def not_subscribing(self, message, flair_id):
        flair = self.set_flair(message.author, flair_id)
        is_subscribing = 0
        is_authenticated = self.citizens_api.is_authenticated(message.body)
        current = None
        highest_rank = self.citizens_api.get_rank(message.body)

        self.update_subscriber_database(
            message.author,
            message.body,
            current,
            highest_rank,
            is_subscribing,
            is_authenticated,
            flair
        )
        if is_authenticated:
            self.send_message('no_subscription_auth', message.author)
        else:
            self.send_message('no_subscription_no_auth', message.author)

    def update_subscriber_database(
            self,
            redditor,
            rsi_username=None,
            current=None,
            highest_rank=None,
            is_subscriber=None,
            is_authenticated=None,
            flair=FlairModel
    ):
        """
        Adds or updates subscribers

        :param redditor:
        :param rsi_username:
        :param current:
        :param highest_rank:
        :param is_subscriber:
        :param is_authenticated:
        :param flair:
        :return:
        """
        subscriber = self.bot.data_manager.query(
            SubscriberModel
        ).filter(
            SubscriberModel.reddit_username == redditor
        ).first()
    
        if not subscriber:
            subscriber = SubscriberModel()
            subscriber.months = 1

        subscriber.reddit_username = redditor
        subscriber.rsi_username = rsi_username
        subscriber.highest_rank = highest_rank
        subscriber.current = 1 if current else 0
        subscriber.months = 1 if current else 0
        subscriber.is_authenticated = 1 if is_authenticated else 0
        subscriber.is_monocle = 0
        subscriber.current = 1 if is_subscriber else 0
        subscriber.flair = flair
        self.bot.data_manager.add(subscriber)


class AuthenticateSubscribersTask(AbstractTaskType):
    """
    Checks for messages with "Subscriber" and handles the result
    ~~~~~~~~~~~~~~~
    MCP
    :license: MIT
    :messages used: 'authentication_success'
    """
    def handle(self, requirements):
        citizen_api = CitizensAPI()
        for awaiting in requirements['awaiting']:
            if citizen_api.is_authenticated(awaiting.rsi_username):
                self.authenticate_subscriber(awaiting)
            else:
                pass

        self.bot.data_manager.commit()
        return True

    def requirements(self):
        awaiting = self.bot.data_manager.query(SubscriberModel).filter(SubscriberModel.is_authenticated == 1)

        requirements = {
            "awaiting": awaiting,
        }
        return requirements

    def authenticate_subscriber(self, subscriber=SubscriberModel):
        """
        Updates the DB, sets flair and sends message

        :param subscriber:
        :return:
        """
        subscriber.is_authenticated = 1
        self.bot.data_manager.add(subscriber)
        self.send_message('authentication_success', subscriber.reddit_username)


class UpdateFlairTask(AbstractTaskType):
    """
    Updates a users flair based on a choice from them
    MCP
    :license: MIT
    :messages used: 'flair_update_success', 'rank_not_high_enough'
    """

    def handle(self, requirements):
        """
        Checks the db to see for any updated RSI info and updates the db accordingly
        Sets the flair based on the choice
        :param requirements:
        :return:
        """
        for message in requirements['messages']:
            flair = self.bot.data_manager.query(FlairModel).filter(FlairModel.name == message.body).first()
            subscriber = self.bot.data_manager.query(
                SubscriberModel
            ).filter(
                SubscriberModel.reddit_username == message.author
            )
            citizens_api = CitizensAPI()

            for rank, value in citizens_api.titles.items():
                if value == subscriber.highest_rank:
                    highest_rank = rank

            if subscriber.highest_rank >= flair.required_rank:
                subscriber.flair = flair
                self.bot.data_manager.add(subscriber)
                self.send_message(
                    'flair_update_success',
                    user_name=message.author,
                    new_flair=flair.name,
                    highest_rank=highest_rank
                )
            else:
                self.send_message(
                    'rank_not_high_enough',
                    user_name=message.author,
                    new_flair=flair.name,
                    highest_rank=highest_rank
                )
        self.bot.data_manager.commit()
        return True

    def requirements(self):
        """
        Needs a message from the user with the subject Flair
        :return messages:
        """
        flair_messages = self.match_unread('Flair')
        if flair_messages:
            return {'messages': flair_messages}
        return False


class UpdateDBTask(AbstractTaskType):
    """
    Runs through the subscribers and checks the current status, ammands the bd as needed
    """

    def handle(self, requirements):
        """
        For every entry checks if subscriber and if monocle and updates the db if it has changed, lets the user know and
        offers flair. Also adds 1 to the months and if the months is now > 12 offer flair

        :param requirements:
        :return:
        """
        pass

    def requirements(self):
        """
        Checks to see if it's the 15th

        :return bool:
        """
        if datetime.datetime.today().day == 15:
            return True
        return False
