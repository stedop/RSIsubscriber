#!/usr/bin/env python
# -*- coding:  utf-8 -*-
# encoding=utf8

"""
TheBot - Acts as an accessor and builer for the the various tools we need, will probably be extended to3
allow for different orm's or add standard api's

Todo add a template manager
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""
from Bot import ConfigManager
from Bot import MessageNotFoundException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from praw.handlers import MultiprocessHandler
from DataModels import MessagesModel
from DataModels import FlairModel
from mako.template import Template
import praw
import logging
import atexit
import re


class BNBot:
    config = ConfigManager
    data_manager = session.Session
    __db_engine = create_engine
    reddit = praw.Reddit
    logger = logging
    mod_list = []
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

        # atexit.register(self.__close_conns())

    def match_unread(self, subject):
        """
        Matches any unread messages with the subject variable and returns then as a dict

        :param subject:
        :return:
        """
        self.logger.debug("SUBJECT = " + str(subject))
        self.logger.debug("MATCH = " + str([message for message in self.reddit.get_unread(limit=None)
            if re.match(subject, message.subject, re.IGNORECASE)]))
        messages = [
            message for message in self.reddit.get_unread(limit=None)
            if re.match(subject, message.subject, re.IGNORECASE)
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
        flair = self.data_manager.query(FlairModel).get(flair_id)
        if flair:
            self.reddit.set_flair(self.config.get("reddit.subreddit"), user_name, flair.text, flair.css_class)
            return flair

        return False

    def is_mod(self, user_name):
        """
        Checks to see if a user is a mod of the config subreddit
        :param user_name:
        :return:
        """
        if len([mod for mod in self.mod_list if mod == str(user_name)]) > 0:
            return True

        return False

    def __get_mods(self):
        """
        Gets all of the mods for the subreddit

        :return:
        """
        for mod in self.reddit.get_subreddit(self.config.get("reddit.subreddit")).get_moderators():
            self.mod_list.append(mod.name)

    def __setup_data_manager(self):
        """
        Sets up the data_manager

        :return:
        """
        Session = sessionmaker()
        self.__db_engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                self.config.get("database.user"),
                self.config.get("database.pass"),
                self.config.get("database.host"),
                self.config.get("database.name")
            ),
            encoding='utf8'
        )
        self.data_manager = Session(bind=self.__db_engine)

    def __setup_reddit_conn(self):
        """
        Inits the reddit connection

        :return:
        """
        user_agent = (self.config.get("reddit.bot_name"))
        handle = MultiprocessHandler('127.0.0.1', 65000)
        self.reddit = praw.Reddit(
            user_agent=user_agent,
            log_requests=self.config.get('reddit.log_requests'),
            handle=handle,
            site_name=self.config.get('reddit.site_name')
        )

        if not self.reddit.refresh_access_information(update_session=True):
            raise RuntimeError

    def __close_conns(self):
        """
        Closes all connections

        :return:
        """
        self.data_manager.close()
