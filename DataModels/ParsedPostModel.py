#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Description
Models need to be parsed and put together, this saves time on that, if it has been parsed before and not updated
~~~~~~~~~~~~~~~
:license: MIT
:author: Stephen Dop
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from DataModels import base
import datetime


class ParsedPostModel(base):
    __tablename__ = 'rsisubs_parsed_posts'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('rsisubs_posts.id'))
    parsed_text = Column(String, nullable=True)
    last_update = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    post = relationship("PostModel")