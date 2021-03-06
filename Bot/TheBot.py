#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# encoding=utf8

"""
MCP
:license: MIT
"""
from Bot import ConfigManager
from Bot import MessageNotFoundException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
#from praw.handlers import MultiprocessHandler
from DataModels import MessagesModel, FlairModel
from mako.template import Template
import praw
import logging
import re


class BNBot(object):
    """
    TheBot - Acts as an accessor and builder for the the various tools we need, will probably be extended to3
    allow for different ORM's or add standard API's
    """
    config = ConfigManager
    data_manager = session.Session
    __db_engine = create_engine
    reddit = praw.Reddit
    logger = logging
    mod_list = []
    data = {}
    BASEDIR = "./"

    def __init__(self, basedir, config_file, logger=logging):
        """
        Sets up th config manager, standard data manager and the praw connection
        :param basedir:
        :param config_file:
        :param logger:
        :return:
        """
        self.BASEDIR = basedir
        self.config = ConfigManager(self.BASEDIR + config_file)
        self.logger = logger

        self.__setup_reddit_conn()
        self.__get_mods()

        if self.config.section_exists('database'):
            self.__setup_data_manager()
        else:
            self.data_manager = None

    def match_unread(self, subject):
        """
        Matches any unread messages with the subject variable and returns then as a dict

        :param subject:
        :return:
        """
        self.logger.debug("SUBJECT = " + str(subject))
        #self.logger.debug("MATCH = " + str([message for message in self.reddit.inbox.unread(limit=None)
        #    if re.match(re.escape(subject), message.subject, re.IGNORECASE)]))
        messages = [
            message for message in self.reddit.inbox.unread(limit=None)
            if re.match(re.escape(subject), message.subject, re.IGNORECASE)
            ]
        if sum(1 for i in messages) != 0:
            return messages

        return False

    def send_message(self, template_name=None, user_name=None, **template_values):
        """
        Sends message to the user from the templates db
        :param template_name:
        :param user_name:
        :param template_values:
        :return:
        """
        if template_name:
            message = self.data_manager.query(
                            MessagesModel
                        ).filter(
                            MessagesModel.name == template_name
                        ).first()

            if message:
                template_values.update(reddit_username=user_name)
                body = Template(
                    message.body.decode('utf8'),
                    input_encoding='utf8',
                    output_encoding='utf8',
                    encoding_errors='ignore',
                    strict_undefined=True
                ).render(**template_values)

                self.reddit.send_message(user_name, message.subject, body)
            else:
                raise MessageNotFoundException("Message with the name " + template_name + " not found")
        return True

    def set_flair(self, user_name, flair_id):
        """
        Sets a users flair based on a db entry
        Also why do I keep spelling flair "fliar"
        :param user_name:
        :param flair_id:
        :return:
        """
        flair = self.data_manager.query(FlairModel).get_value(flair_id)

        if self.is_mod(user_name):
            css_class = flair.css_class + " mod"
        else:
            css_class = flair.css_class

        if flair:
            self.reddit.set_flair(self.config.get_value("reddit.subreddit"), user_name, flair.text, css_class)
            return flair

        return False

    def set_explicit_flair(self, user_name, flair, css_class = None):
        """
        Sets a user flair based on the string passed in.
        :param user_name:
        :param flair:
        :param css_class:
        :return:
        """
        if flair:
            if css_class:
                self.reddit.set_flair(self.config.get_value("reddit.subreddit"), user_name, flair, css_class)
            else:
                self.reddit.set_flair(self.config.get_value("reddit.subreddit"), user_name, flair)

        return True
    
    def delete_flair(self, user_name):
        """
        Deletes the user's current flair.
        :param user_name:
        :return:
        """
        self.reddit.delete_flair(self.config.get_value("reddit.subreddit"),  user_name)

    def get_flair(self, user_name):
		"""
		Returns the current user flair.
		:param user_name:
		:return:
		"""
		flair = self.reddit.subreddit(self.config.get_value("reddit.subreddit")).flair(user_name)
		if flair:
			return next(flair)
		return None

    def is_mod(self, user_name):
        """
        Checks to see if a user is a mod of the config subreddit
        :param user_name:
        :return:
        """
        if [mod for mod in self.mod_list if mod == str(user_name)] is False:
            return True

        return False

    def __get_mods(self):
        """
        Gets all of the mods for the subreddit

        :return:
        """
        for mod in self.reddit.subreddit(self.config.get_value("reddit.subreddit")).moderator():
            self.mod_list.append(mod.name)

    def __setup_data_manager(self):
		"""
		Sets up the data_manager
        :return:
		"""
		session = sessionmaker()
		self.__db_engine = create_engine(
			"mysql+mysqldb://{user}:{password}@{host}/{db_name}".format(
				user=self.config.get_value("database.user"),
				password=self.config.get_value("database.pass"),
				host=self.config.get_value("database.host"),
				db_name=self.config.get_value("database.name")
			),
			encoding='utf8'
		)
		self.data_manager = session(bind=self.__db_engine)

    def __setup_reddit_conn(self):
        """
        Inits the reddit connection

        :return:
        """
        user_agent = (self.config.get_value("reddit.bot_name"))
        #handle = MultiprocessHandler('127.0.0.1', 65000)
        self.reddit = praw.Reddit(site_name=self.config.get_value('reddit.site_name'),
            user_agent=user_agent,
            log_requests=self.config.get_value('reddit.log_requests')
        )

        #if not self.reddit.refresh_access_information(update_session=True):
        #    raise RuntimeError
