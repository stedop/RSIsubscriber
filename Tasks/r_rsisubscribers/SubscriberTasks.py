#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Subscription tasks
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""

from src.TasksManager import AbstractTaskType
from DataModels.SubscribersAPI import SubscribersAPI
from DataModels.SubscriberModel import SubscriberModel
from DataModels.FlairModel import FlairModel


class CheckSubscriberMessagesTask(AbstractTaskType):
    """
    Checks for messages with "Subscriber" and handles the result
    ~~~~~~~~~~~~~~~
    MCP
    :license: MIT
    :messages used: 'subscription_auth_monocle',
                    'subscription_auth',
                    'subscription_not_auth',
                    'subscriber_not_found'
    """
    def handle(self, requirements):
        """
        Handle the messages
        :return:
        """
        messages = requirements['messages']
        subscribers_api = (requirements['subscribers'])
        for message in messages:
            is_subscriber = subscribers_api.is_subscriber(message.body)
            if is_subscriber:
                is_authenticated = subscribers_api.is_authenticated(message.author)
                is_monocle = subscribers_api.is_monocle(message.author)
                flair_id = 2

                if is_authenticated and is_monocle:
                    flair_id = 1
                    self.send_message('subscription_auth_monocle', message.author)
                elif is_authenticated and not is_monocle:
                    flair_id = 1
                    self.send_message('subscription_auth', message.author)
                elif not is_authenticated and not is_monocle:
                    self.send_message('subscription_not_auth', message.author)

                flair = self.set_flair(message.author, flair_id)
                self.update_subscriber_database(
                    message.author,
                    message.body,
                    is_subscriber,
                    is_authenticated,
                    is_monocle,
                    flair
                )
            else:
                self.send_message('subscriber_not_found', message.author)

        # Commits and DB changes
        self.bot.data_manager.commit()
        return True

    def requirements(self):
        """
        Get Subscriber Messages
        :return:
        """
        sbuscriber_messages = self.match_unread('Subscriber')
        if sbuscriber_messages:
            return {'messages': sbuscriber_messages, 'subscribers': SubscribersAPI()}
        return False
    
    def update_subscriber_database(self, reddit_user_name, rsi_username=None, is_subscriber=None, is_authenticated=None, is_monocle=None, flair=FlairModel):
        """
        Adds or updates subscribers
        :param reddit_user_name:
        :param rsi_username:
        :param is_subscriber:
        :param is_authenticated:
        :param is_monocle:
        :param flair FlairModel:
        :return:
        """
        subscriber = self.bot.data_manager.query(
            SubscriberModel
        ).filter(
            SubscriberModel.reddit_username == reddit_user_name
        ).first()
    
        if not subscriber:
            subscriber = SubscriberModel()
            subscriber.months = 1

        subscriber.reddit_username = reddit_user_name
        subscriber.rsi_username = rsi_username
        subscriber.is_monocle = 1 if is_monocle else 0
        subscriber.authenticated = 1 if is_authenticated else 0
        subscriber.current = 1 if is_subscriber else 0
        subscriber.flair = flair

        self.bot.data_manager.add(subscriber)


class AuthenticateSubscribersTask(AbstractTaskType):
    """
    Checks for messages with "Subscriber" and handles the result
    ~~~~~~~~~~~~~~~
    MCP
    :license: MIT
    :messages used:
    """
    def handle(self, requirements):
        api = requirements['subscribers']
        for awaiting in requirements['awaiting']:
            if api.is_authenticated(awaiting.rsi_username):
                self.authenticate_subscriber()
            else:
                pass

        self.bot.data_manager.commit()
        return True

    def requirements(self):
        awaiting = self.bot.data_manager.query(SubscriberModel).filter(SubscriberModel.is_authenticated).get()

        requirements = {
            "awaiting": awaiting,
            'subscribers': SubscribersAPI()
        }
        return requirements

    def authenticate_subscriber(self, subscriber=SubscriberModel):
        """
        Updates the DB, sets flair and sends message
        :param subscriber SubscriberModel:
        :return:
        """
        subscriber.is_authenticated = 1
        self.bot.data_manager.update(subscriber)
        self.send_message('auth', subscriber.reddit_username)