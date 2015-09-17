#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from src.TasksManager import AbstractTaskType
from src.TheBot import Bot
from rsisubscribers.SubscribersAPI import SubscribersAPI

tasks = [SubscriptionTask]
myBot = Bot('rsi_config.ini', tasks)
