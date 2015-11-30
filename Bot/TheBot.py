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
from Bot.ConfigManager import ConfigManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from praw.handlers import MultiprocessHandler
from DataModels.MessagesModel import MessagesModel
from DataModels.FlairModel import FlairModel
from mako.template import Template
from Bot.Exceptions import MessageNotFoundException
import praw
import logging


class Bot:
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
        self.logger.info(self.config.get('reddit.config_file'))
        self.logger.info(self.BASEDIR + self.config.get('reddit.config_file'))
        if self.config.section_exists('database'):
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
        else:
            self.data_manager = None

        user_agent = (self.config.get("reddit.bot_name"))
        handle = MultiprocessHandler('127.0.0.1', 65000)

        self.reddit = praw.Reddit(
            user_agent=user_agent,
            log_requests=self.config.get('reddit.log_requests'),
            handle=handle,
            config_file=self.config.get('reddit.config_file')
        )
        self.logger.warn(self.config.get('reddit.config_file'))

        if not self.reddit.refresh_access_information():
            raise RuntimeError
        # atexit.register(self.close_conns, self.r, self.data_manager)

        for mod in self.reddit.get_subreddit(self.config.get("reddit.subreddit")).get_moderators():
            self.mod_list.append(mod.name)

    def match_unread(self, subject):
        """
        Matches any unread messages with the subject variable and returns then as a dict

        :param subject:
        :return:
        """
        messages = self.reddit.get_unread(
            [message for message in self.reddit.get_unread(limit=None) if message.subject == subject]
        )
        return messages

    def send_message(self, template_name=None, user_name=None, **template_values):
        """
        Sends message to the user from the templates db
        :param template_name:
        :param user_name:
        :param template_values:
        :return:
        """
        if template_name:
            self.logger.info("Template name: " + template_name)
            message = self.data_manager.query(
                            MessagesModel
                        ).filter(
                            MessagesModel.name == template_name
                        ).first()
            if message:
                template_values.update(reddit_username=user_name)
                self.logger.debug(template_values)

                body = Template(
                    message.body.decode('utf8'),
                    input_encoding='utf8',
                    output_encoding='utf8',
                    encoding_errors='ignore'
                ).render(**template_values)

                self.reddit.send_message(user_name, message.subject, body)
            else:
                raise MessageNotFoundException("Message with the name " + template_name + " not found")
                pass
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
        if user_name in self.mod_list:
            return True

        return False