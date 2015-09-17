#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class MessagesModel(Base):
    __tablename__ = 'rsisubs_messages'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)
    body = Column(String)