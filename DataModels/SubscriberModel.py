#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from DataModels import Base


class SubscriberModel(Base):
    __tablename__ = 'rsisubs_subscribers'

    id = Column(Integer, primary_key=True)
    flair_id = Column(Integer, ForeignKey('rsisubs_flair.id'))
    reddit_username = Column(String)
    rsi_username = Column(String)
    months = Column(Integer)
    current = Column(Integer)
    is_monocle = Column(Integer)
    is_authenticated = Column(Integer)
    flair = relationship("FlairModel")

    def has_subscribed(self):
        if self.is_subscribed == 1:
            return True
        return False