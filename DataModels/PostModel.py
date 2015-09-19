#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Description
~~~~~~~~~~~~~~~
Mod Generated Post Model
:license: MIT
:author: Stephen Dop
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from DataModels import Base


class PostModel(Base):
    __tablename__ = 'rsisubs_posts'

    id = Column(Integer, primary_key=True)
    creator_username = Column(String)
    post_title = Column(String)
    post_body = Column(String)
    last_time_completed = Column(DateTime)
    reoccurring_unit = Column(String)  # "Days", "Weeks", "Month" etc.
    reoccurring_every_x = Column(String)  # Reoccurring interval
    last_update = Column(DateTime)
    links = relationship("LinksModel")
    parsed_post = relationship("ParsedPostModel")