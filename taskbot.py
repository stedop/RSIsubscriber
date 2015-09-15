#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from src.ConfigManager import ConfigManager


"""tm = RedditTaskManager("Task Bot", ConfigManager("rsi_config.ini"))
tm.run()"""

configMan = ConfigManager("rsi_config.ini")
botName = configMan.get("bot_name")