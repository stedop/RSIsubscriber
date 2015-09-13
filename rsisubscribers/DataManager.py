#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import sqlalchemy

class Subscriber():
    id = []
    reddit_username = []
    rsi_username = []
    months = 0
    is_subscribed = 0
    is_monocle = 0
    HASONE = ['flair']

class Flair():
    id = []
    css_class = ""
    text = ""
    BELONGSTO = ['subscriber']

Registry.register(Subscriber, Flair)