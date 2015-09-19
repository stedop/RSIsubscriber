#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
TheBot
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
    r = praw.Reddit

    def __init__(self, config_file):
        self.config = ConfigManager(config_file)

        if self.config.section_exists('database'):
            Session = sessionmaker()
            self.__db_engine = create_engine(
                "mysql+mysqldb://{}:{}@{}/{}".format(
                    self.config.get('database.user'),
                    self.config.get('database.pass'),
                    self.config.get('database.host'),
                    self.config.get('database.name')
                )
            )
            print(type(Session(bind=self.__db_engine)))
            self.data_manager = Session(bind=self.__db_engine)


        user_agent = (self.config.get("reddit.bot_name"))
        handle = MultiprocessHandler()

        self.r = praw.Reddit(
            user_agent=user_agent,
            log_requests=self.config.get('reddit.log_requests'),
            handle=handle,
            config_file=self.config.get('reddit.config_file')
        )

        if not self.r.refresh_access_information():
            raise RuntimeError
        # atexit.register(self.close_conns, self.r, self.data_manager)
