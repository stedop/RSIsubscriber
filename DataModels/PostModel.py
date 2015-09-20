#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Description
~~~~~~~~~~~~~~~
Mod Generated Post Model
:license: MIT
:author: Stephen Dop
"""

from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.orm import relationship
from DataModels import Base
import datetime


class PostModel(Base):
    __tablename__ = 'rsisubs_posts'

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