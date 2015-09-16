#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from src.ConfigManager import ConfigManager
from src.TasksManager import RedditTaskManager

tm = RedditTaskManager("Task Bot", ConfigManager("rsi_config.ini"))
tm.run()
