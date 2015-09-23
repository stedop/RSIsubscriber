#!/usr/bin/env python
# -*- coding:  utf-8 -*-


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from DataModels import Base

class FlairModel(Base):
    __tablename__ = 'rsisubs_flair'

    id = Column(Integer, primary_key=True)
    required_rank = Column(Integer)
    name = Column(String)
    css_class = Column(String)
    text = Column(String)
    subscribers = relationship("SubscriberModel")