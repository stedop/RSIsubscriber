#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Description
~~~~~~~~~~~~~~~
Links for Posts
:license: MIT
:author: Stephen Dop
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from DataModels import Base


class LinksModel(Base):
    __tablename__ = 'rsisubs_post_links'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('rsisubs_posts.id'))
    uri = Column(String, nullable=False)
    alt = Column(String, nullable=False)
    description = Column(String, nullable=True)
    level = Column(Integer, nullable=False, default=999)
    suggested_by = Column(String, nullable=False)
    post = relationship("PostModel")