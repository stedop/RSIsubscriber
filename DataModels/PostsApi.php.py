#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Description
~~~~~~~~~~~~~~~
An API for Posts - This is going to parse a post from the db and put together the final text,
it's also going to get scheduled posts from the db
:license: MIT
:author: Stephen Dop
"""

from Bot.TheBot import Bot
from DataModels.PostModel import PostModel
from datetime import datetime
from sqlalchemy import func


class PostsApi():
    __bot = Bot

    def __init__(self, bot=Bot):
        self.__bot = bot

    def get_all_posts(self):
        """
        Gets every post
        :return:
        """
        return self.__bot.data_manager.query(PostModel).filter(PostModel.archived == 0)

    def get_scheduled_posts(self, date=datetime or None):
        if not date:
            date = func.now()

        # Todo turn the following sql into a alchemy layout (use .func)
        # "SELECT * FROM `posts WHERE `last_completed` + INTERVAL `reoccurring_interval` `reoccurring_unit` >= " + date

        scheduled = self.__bot.data_manager.query(
            PostModel
        ).whereclause(
            "`last_completed` + INTERVAL `reoccurring_interval` `reoccurring_unit` >= " + date
        )

        return scheduled

    def make_post(self, post_id):
        pass

    def is_parsed(self, post_id):
        pass