#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Subscription tasks
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""

from Bot.TasksManager import AbstractTaskType
from datetime import datetime, timedelta
import time
import urllib2
import re
from DataModels.TradebotModels import Trade, User, UserAudit
from Utils.Model import Model
from Utils.SubHTMLParser import SubHTMLParser
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, joinedload

"""
Get private messages and update reddit user flair with RSI profile name.
"""
class ConfirmCitizenTask(AbstractTaskType):

	def handle(self, requirements):
		messages = requirements['messages']
		subreddit_name = self.bot.config.get_value('reddit.subreddit')
		subreddit = self.bot.reddit.get_subreddit(subreddit_name)
		
		for message in messages:
			try:
				author = str(message.author)
				current_flair = self.bot.get_flair(author)

				# only set flair if author doesn't have existing flair
				if current_flair and current_flair["flair_text"]:
					self.bot.logger.debug("** ERROR: [USERFLAIR]: duplicate flair request received from: {0}".format(message.author))
					self.bot.reddit.send_message(message.author, "starcitizen_trades bot: problem with your flair request", "Sorry, it appears your flair was already set previously. If you have a problem with your existing flair then please [click here to message the mods](http://www.reddit.com/message/compose?to=%2Fr%2FStarcitizen_trades).")
					return

				bodylines = message.body.splitlines()

				# only recognize well-formed message requests
				if not bodylines:
					self.bot.logger.debug("** ERROR: [USERFLAIR]: improperly formatted flair request received from {0}".format(message.author))
					self.bot.reddit.send_message(message.author, "starcitizen_trades bot: problem with your flair request", "Sorry, it appears your flair request isn't formatted correctly.  Did you follow the guidelines? Please ensure you followed all the steps correctly and try again. If you're still running into problems then please [click here to message the mods](http://www.reddit.com/message/compose?to=%2Fr%2FStarcitizen_trades).")
					return

				rsi_name = bodylines[0]

				try:
					rsi_page_response = urllib2.urlopen("https://www.robertsspaceindustries.com/citizens/" + rsi_name)
					rsi_page_content = rsi_page_response.read()
				except urllib2.HTTPError:
					self.bot.logger.debug("** ERROR: [USERFLAIR]: couldn't access RSI profile page for {0} from reddit user {1}".format(rsi_name, message.author))
					self.bot.reddit.send_message(message.author, "starcitizen_trades bot: problem with your flair request", "Sorry, I couldn't find an RSI profile for the handle you provided.  Did you follow the guidelines? If you're still running into problems then please [click here to message the mods](http://www.reddit.com/message/compose?to=%2Fr%2FStarcitizen_trades).")
					return

				# Try to match reddit link, with /u/ or /user/, plus optional single trailing slash and unlimited trailing whitespace.
				# Do not match if link isn't on its own line, to prevent (unlikely) username spoofing based on substrings.
				# Valid examples:
				#      "reddit.com/user/foo   "
				#      "http://reddit.com/u/foo/"
				reddit_user_match = re.search(r"reddit.com/u(ser)?/" + author + "/?\s*(<br />)?\\n", rsi_page_content, re.IGNORECASE)
				
				# Try to find the citizen ID number.
				parser = SubHTMLParser()
				parser.feed(rsi_page_content)
				uee_number = parser.citizen_number

				if reddit_user_match:
					# Look for a request to be flagged as a Broker, otherwise default to Trader
					role = "Trader"

					if ((len(bodylines) > 1 and re.match("Broker", bodylines[1], re.I)) or (len(bodylines) > 2 and re.match("Broker", bodylines[2], re.I))):
						role = "Broker"

					# RSI link was valid, so set flair
					subreddit.set_flair(author, "RSI {0}, {1}".format(rsi_name, role))
					self.bot.logger.debug("set flair for {0} to {1} as {2}".format(author, rsi_name, role))
					# send success message to author
					self.bot.reddit.send_message(message.author, "starcitizen_trades bot: flair set", "Congratulations, everything appears to be in order and your flair is now set! If it doesn't appear in the next few minutes, then please [click here to message the mods](http://www.reddit.com/message/compose?to=%2Fr%2FStarcitizen_trades).")

					user = self.bot.data_manager.query(User).filter(User.user_id == author).first()
					if not user:
						user = Model.create_user(author, "RSI {0}, {1}".format(rsi_name, role))
					else:
						user.title = "RSI {0}, {1}".format(rsi_name, role)
					
					user.citizen_id = uee_number

					# Create the audit record for the user.
					user_audit = Model.create_user_audit(user)

					self.bot.data_manager.add(user)
					self.bot.data_manager.add(user_audit)
				
				else:
					# send error message to author
					self.bot.logger.debug("** ERROR: [USERFLAIR]: attempted to link invalid RSI profile {0} from reddit user {1}".format(rsi_name, message.author))
					self.bot.reddit.send_message(message.author, "starcitizen_trades bot: problem with your flair request", "Sorry, it appears your RSI profile doesn't include a correct link to your reddit user page.  Did you follow the guidelines?  Please ensure you followed all the steps correctly and try again.  If you're still running into problems then please [click here to message the mods](http://www.reddit.com/message/compose?to=%2Fr%2FStarcitizen_trades).")

			except Exception as not_found:
				self.bot.logger.exception(not_found)
				self.bot.data_manager.rollback()
				continue
			finally:
				self.bot.data_manager.commit()
				message.mark_as_read()

		return True
		
	"""
	Get private messages and filter by subject.
	:return:
	"""
	def requirements(self):
		messages = self.bot.match_unread('flair request')
		if messages:
			return {'messages': messages}
		return False

"""
tradebot - Private message that indicates whether the user wants to show or hide their trade flair.
"""
class ShowHideFlairTask(AbstractTaskType):

	def handle(self, requirements):
		add_flair_names = []
		remove_flair_names = []

		messages = requirements['messages']

		# Read through the messages.
		for message in messages:
			try:
				if message.body == "show":
					self.bot.data_manager.query(User).\
						filter(User.user_id == message.author.name).update({User.flair_ind: '1'})
					# Add the reddit name because we know we need to update it later.
					if message.author.name not in add_flair_names:
						add_flair_names.append(message.author.name)
				elif message.body == "hide":
					self.bot.data_manager.query(User).\
						filter(User.user_id == message.author.name).update({User.flair_ind: '0'})
					if message.author.name not in remove_flair_names:
						remove_flair_names.append(message.author.name)

			except Exception as e:
				self.bot.logger.exception("{}".format(datetime.utcnow()))
			finally:
				message.mark_as_read()

		self.bot.data.update({'updated': add_flair_names})
		self.bot.data.update({'removed': remove_flair_names})

		return True

	def requirements(self):
		messages = self.bot.match_unread('+flair')
		if messages:
			return {'messages': messages}
		return False

"""
tradebot - Private message to reset their flair.
"""
class RemoveFlairTask(AbstractTaskType):
	def handle(self, requirements):
		messages = requirements['messages']

		for message in messages:
			try:
				current_time = datetime.utcnow()
				updated = []
				prior_flair = []
				redditor = message.author
				flair = self.bot.get_flair(redditor.name)
				if not flair:
					self.bot.reddit.send_message(redditor, "starcitizen_trades bot: flair removal request",  "No existing flair found. Please follow the directions [here](https://www.reddit.com/r/Starcitizen_trades/wiki/userconfirmation) to become verified.")
					return
				prior_flair.append(flair)
				user = self.bot.data_manager.query(User).filter(User.user_id == redditor.name).first()
				update_dtm = None
				override = False
				if not user:
					user = Model.create_user(redditor.name, flair)
					update_dtm = current_time
					override = True
				else:
					# Update the current user
					user.title = flair
					update_dtm = user.update_dtm
					#update_dtm = datetime.strptime(user.update_dtm,  "%Y-%m-%d %H:%M:%S")
					user.update_dtm = current_time
					
				# Calculate if the required minimum time has passed.
				diff = current_time - update_dtm
				if diff > timedelta(30) or override:
					# Create the audit record for the user.
					user_audit = Model.create_user_audit(user)

					self.bot.data_manager.add(user)
					self.bot.data_manager.add(user_audit)
					# Commit for now after every message - may need to change to group commit for performance
					self.bot.data_manager.commit()

					self.bot.delete_flair(redditor.name)
					self.bot.reddit.send_message(redditor, "starcitizen_trades bot: flair removed", "Congratulations, your flair has been reset. To find out how to add back any confirmed trades, please [click here](https://www.reddit.com/r/Starcitizen_trades/wiki/tradebot#wiki_commands).")
					updated.append(redditor.name)
					self.bot.data.update({'flair_removed': updated})
					self.bot.data.update({'old_flair': prior_flair})
				else:
					self.bot.reddit.send_message(redditor, "starcitizen_trades bot: flair removal request",  "Your flair has been updated within the past 30 days. Please [click here](http://www.reddit.com/message/compose?to=%2Fr%2FStarcitizen_trades) to message the mods with your request.")

			except Exception as e:
				self.bot.logger.exception("{}".format(datetime.utcnow()))
				self.bot.data_manager.rollback()
			finally:
				self.bot.data_manager.close()
				message.mark_as_read()

	def requirements(self):
		messages = self.bot.match_unread('flair remove')
		if messages:
			return {'messages': messages}
		return False
