#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from twistar.dbobject import DBObject
from twistar.registry import Registry

class Subscriber(DBObject):
    id = []
    reddit_username = []
    rsi_username = []
    months = 0
    is_subscribed = 0
    is_monocle = 0
    HASONE = ['flair']

class Flair(DBObject):
    id = []
    css_class = ""
    text = ""
    BELONGSTO = ['subscriber']

Registry.register(Subscriber, Flair)