#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from config.ConfigManager import ConfigManager
from taks.TasksManager import RedditTaskManager, AbstractRedditTask


"""tm = RedditTaskManager("Task Bot", ConfigManager("rsi_config.ini"))
tm.run()"""

configMan = ConfigManager("rsi_config.ini")
botName = configMan.get("bot_name")