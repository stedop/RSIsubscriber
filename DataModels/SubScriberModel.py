#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from DataModels.FlairModel import FlairModel

Base = declarative_base()


class SubscriberModel(Base):
    __tablename__ = 'rsisubs_subscribers'

    id = Column(Integer, primary_key=True)
    reddit_username = Column(String)
    rsi_username = Column(String)
    months = Column(Integer)
    current = Column(Integer)
    is_monocle = Column(Integer)
    suthenticated = Column(Integer)
    flair_id = Column(Integer, ForeignKey('rsisubs_flair.id'))
    flair = relationship("FlairModel")

    def has_subscribed(self):
        if self.is_subscribed == 1:
            return True
        return False