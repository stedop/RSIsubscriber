#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Description
~~~~~~~~~~~~~~~
Mod Generated Post Model
:license: MIT
:author: Stephen Dop
"""

from sqlalchemy import Column, Integer, String, DateTime, text, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.orm.session import object_session
from DataModels import Base
import datetime


class PostModel(Base):
    __tablename__ = 'rsisubs_posts'

    _session = {}
    id = Column(Integer, primary_key=True)
    creator_username = Column(String)
    post_title = Column(String)
    post_body = Column(String)
    reoccurring_unit = Column(String)  # Must be MySQL standard interval unit
    reoccurring_interval = Column(String)  # Reoccurring interval
    links = relationship("LinksModel")
    parsed_post = relationship("ParsedPostModel")
    last_completed = Column(DateTime(timezone=True))
    last_update = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    archived = Column(DateTime(timezone=True), nullable=True, server_default=text('NULL'))

    def __init__(self):
        self._session = object_session(self)

    def get_all_posts(self):
        """
        Gets every post
        :return:
        """
        return self._session.query(PostModel).filter(PostModel.archived == 0)

    def get_scheduled_posts(self, date=datetime or None):
        if not date:
            date = func.now()

        # Todo turn the following sql into a alchemy layout (use .func)
        # "SELECT * FROM `posts WHERE `last_completed` + INTERVAL `reoccurring_interval` `reoccurring_unit` >= " + date
        scheduled = self._session.query(
            PostModel
        ).whereclause(
            "`last_completed` + INTERVAL `reoccurring_interval` `reoccurring_unit` >= " + date
        )

        return scheduled

    def make_post(self, post_id):
        pass

    def is_parsed(self, post_id):
        pass