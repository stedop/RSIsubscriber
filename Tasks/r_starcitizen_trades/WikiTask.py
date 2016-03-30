#!/usr/bin/env python
# -*- coding:  utf-8 -*-

import praw
from Bot.TasksManager import AbstractTaskType
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class RemovedFlairWikiTask(AbstractTaskType):
	def handle(self,  requirements):
		try:
			subreddit = self.bot.config.get_value('reddit.subreddit')
			wiki = self.bot.reddit.get_wiki_page( subreddit, 'mod/flairbotremoved')
			if wiki:
				content = wiki.content_md
				old_flair = self.bot.data.get('old_flair')
				new_line = ""
				for name in self.bot.data.get('flair_removed'):
					i = 0
					new_line += "\n{} | {} | {}".format(name,  old_flair[i],  datetime.utcnow().strftime(TIME_FORMAT))
					i += 1
				self.bot.reddit.edit_wiki_page(subreddit,  'mod/flairbotremoved',  content + new_line)
		except Exception as e:
			self.bot.logger.exception("{}".format(datetime.utcnow()))
	
	def requirements(self):
		if self.bot.data.get('flair_removed'):
			return True
		
		return False
	
