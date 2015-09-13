#!/usr/bin/env python
# -*- coding:  utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class SubscriberModel(Base):
    __tablename__ = 'subscribers'

    id = Column(Integer, primary_key=True)
    reddit_username = Column(String)
    rsi_username = Column(String)
    months = Column(Integer)
    current = Column(Integer)
    is_monocle = Column(Integer)
    flair_id = Column(Integer, ForeignKey('flair.id'))
    flair = relationship("FlairModel")

    def is_subscriber(self):
        if self.is_subscribed == 1:
            return True
        return False

class FlairModel(Base):
    __tablename__ = 'flair'

    id = Column(Integer, primary_key=True)
    css_class = Column(String)
    text = Column(String)
    subscribers = relationship("SubscriberModel")