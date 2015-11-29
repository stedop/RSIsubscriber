#!/usr/bin/env python
# -*- coding:  utf-8 -*-


from sqlalchemy import Column, Integer, String
from DataModels import Base


class MessagesModel(Base):
    __tablename__ = 'rsisubs_messages'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)
    body = Column(String)
