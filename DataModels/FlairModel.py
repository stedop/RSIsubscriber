#!/usr/bin/env python
# -*- coding:  utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from DataModels.SubScriberModel import SubscriberModel

Base = declarative_base()

class FlairModel(Base):
    __tablename__ = 'rsisubs_flair'

    id = Column(Integer, primary_key=True)
    css_class = Column(String)
    text = Column(String)
    subscribers = relationship("SubscriberModel")