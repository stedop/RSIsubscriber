#!/usr/bin/env python
# -*- coding:  utf-8 -*-

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
import praw


class Bot:
    config = ConfigManager
    data_manager = session.Session
    __db_engine = create_engine
    reddit = praw.Reddit

    def __init__(self, config_file):
        """
        Sets up th config manager, standard data manager and the praw connection
        :param config_file:
        :return:
        """
        self.config = ConfigManager(config_file)

        if self.config.section_exists('database'):
            Session = sessionmaker()
            self.__db_engine = create_engine(
                "mysql+mysqldb://{}:{}@{}/{}".format(
                    self.config.get("database.user"),
                    self.config.get("database.pass"),
                    self.config.get("database.host"),
                    self.config.get("database.name")
                )
            )
            self.data_manager = Session(bind=self.__db_engine)
        else:
            self.data_manager = None

        user_agent = (self.config.get("reddit.bot_name"))
        handle = MultiprocessHandler()

        self.reddit = praw.Reddit(
            user_agent=user_agent,
            log_requests=self.config.get('reddit.log_requests'),
            handle=handle,
            config_file=self.config.get('reddit.config_file')
        )

        if not self.reddit.refresh_access_information():
            raise RuntimeError
        # atexit.register(self.close_conns, self.r, self.data_manager)
