#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tradebot tasks
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""

from Bot.TasksManager import AbstractTaskType
from datetime import datetime
import re
import praw
from string import maketrans
import time
from DataModels.TradebotModels import Trade, User
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, joinedload

"""
Parses the stickied trade thread for the confirmed trades.
"""
class ParseTradesThreadTask(AbstractTaskType):

	def handle(self, requirements):
		redditors = []
		trades = []
		comments = requirements['comments']

		for comment in comments:
			if (isinstance(comment, praw.objects.Comment)) and ("+trade" in comment.body.lower()):
				replies = comment.replies
				for reply in replies:
					if isinstance(reply, praw.objects.MoreComments):
						reply = reply.comments()[0]

					try:
						if ("+verify" in reply.body.lower()) and (comment.author.name != reply.author.name):
							# Add the author to a list if they have been added already.
							if comment.author not in redditors:
								redditors.append(comment.author.name)
							if reply.author not in redditors:
								redditors.append(reply.author.name)

							# Also add the trades to a list.
							if "wtb" in comment.body.lower():
								trade = self.populate_trade(reply, comment, False)
								trades.append(trade)
							else:
								trade = self.populate_trade(comment, reply, True)
								trades.append(trade)
					except praw.errors.NotFound:
						self.bot.logger.exception("{}".format(datetime.utcnow()))

		self.bot.data.update({'confirmed': redditors})
		self.bot.data.update({'trades': trades})

	def requirements(self):
		subreddit = self.bot.reddit.get_subreddit(self.bot.config.get_value('reddit.subreddit'))
		sticky_submission = subreddit.get_hot().next()
		submission = praw.objects.Submission.from_url(self.bot.reddit, sticky_submission.url, comment_limit = 50, comment_sort = 'new')
		comments = submission.comments

		if comments:
			return {'comments': comments}
		return False

	"""
	Finds a specified substring and return the whole string the substring was in.
	"""
	def find_and_return(self, key, message):
		index = message.find(key)
		if index > -1:
			end_index = message.find(" ", index)
			# Means newline char or there is nothing else after this.
			if end_index < 0:
				end_index = len(message)
			value = message[index:end_index]
			values = value.split(":")
			return values[1]
		else:
			return None

	"""
	Returns a new Trade object with the class variables populated.
	"""
	def populate_trade(self, sale_comment, buy_comment, top):
		URL_REGEX = re.compile("reddit.com/r/" + self.bot.config.get_value('reddit.subreddit') + "/comments/\w+/\w+/?")

		sale_url_info = re.search(URL_REGEX, sale_comment.body)
		if sale_url_info == None:
			sale_url_info = re.search(URL_REGEX, buy_comment.body)
		sale_submission_url = None
		if sale_url_info != None:
			sale_submission_url = sale_url_info.group()

		# Find any optional values here.
		item = self.find_and_return("+item", sale_comment.body)
		insurance = None
		# If it's a ship, format will be +item:<ship>[insurance], i.e. +item:Aurora[LTI]
		if (item != None and "[" in item and "]" in item):
			start = item.find("[")
			end = item.find("]")
			insurance = item[start + 1:end]
			item = item[:start]
	
		price_value = None
		price_currency = None
		price = self.find_and_return("+price", sale_comment.body)
		# Format for the price is +price:<amount><currency>, i.e. +price:1,000USD
		if price != None:
			# Gets rid of the commas.
			price = price.translate(translation_table)
			price_value_group = re.search("\d+", price)
			if price_value_group != None:
				price_value = price_value_group.group(0)
			price_currency_group = re.search("\D+", price)
			if price_currency_group != None:
				price_currency = price_currency_group.group(0)

		# Now populate the Trade object.
		trade = Trade()
		trade.submission_id = sale_comment.submission.id
		trade.comment_id = sale_comment.id
		trade.seller_id = sale_comment.author.name
		trade.buyer_id = buy_comment.author.name
		trade.item = item
		trade.insurance = insurance
		trade.amount = price_value
		trade.currency = price_currency
		if sale_submission_url != None:
			trade.sale_link = "http://www." + sale_submission_url
		if top == True:
			trade.comment_link = sale_comment.permalink
		else:
			trade.comment_link = buy_comment.permalink

		return trade

"""
Saves the redditor and any trades.
"""
class SaveDataTask(AbstractTaskType):

	def handle(self, requirements):
		actual_updated = set()
		redditors = self.bot.data.get('confirmed')

		try:
			for name in redditors:
				result = self.bot.data_manager.query(exists().where(User.user_id == name)).scalar()
				if not result:
					user = self.populate_user(name)
					self.bot.data_manager.add(user)

			trades = self.bot.data.get('trades')
			for trade in trades:
				result = self.bot.data_manager.query(and_(exists().where(Trade.submission_id == trade.submission_id),\
					exists().where(Trade.comment_id == trade.comment_id))).scalar()
				if not result:
					self.bot.data_manager.add(trade)
					actual_updated.add(trade.seller_id)
					actual_updated.add(trade.buyer_id)

			self.bot.data_manager.commit()
		except Exception as e:
			self.bot.logger.exception("{}".format(datetime.utcnow()))
			self.bot.data_manager.rollback()
		finally:
			self.bot.data.update({'flaired': actual_updated})

	def requirements(self):
		return True

	"""
	Returns a new User object with the class variables populated.
	"""
	def populate_user(self, name):
		user = User()
		user.user_id = name
		flair = self.bot.get_flair(name)
		user.title = flair
		user.flair_ind = "1"

		return user

"""
Updates user flair with the number of confirmed trades.
"""
class UpdateTradeFlairTask(AbstractTaskType):

	def handle(self, requirements):
		try:
			flair_names = self.bot.data.get('flaired')
			flair_updated = self.bot.data.get('updated')
			if flair_names and flair_updated:
				unique_names = flair_names | set(flair_updated)
			elif flair_names:
				unique_names = flair_names
			else:
				unique_names = flair_updated

			if unique_names:
				sellers = self.bot.data_manager.query(Trade.seller_id.label("name")).filter(Trade.seller_id.in_(unique_names))
				buyers = self.bot.data_manager.query(Trade.buyer_id.label("name")).filter(Trade.buyer_id.in_(unique_names))
				users = self.bot.data_manager.query("name", func.count("name")).select_from(union_all(sellers, buyers).\
					alias("reputation")).group_by("name").all()

				for user in users:
					try:
						flair_ind = self.bot.data_manager.query(User.flair_ind).filter(User.user_id == user[0]).scalar()
						if flair_ind == "1":
							existing_flair = self.bot.get_flair(user[0])
							if existing_flair is None:
								continue
							else:
								trade_index = existing_flair.find("Trades:")
								if trade_index > 1:
									flair_text = existing_flair[:trade_index - 2] + ", Trades: {}"
								else:
									flair_text = existing_flair + ", Trades: {}"

							self.bot.set_explicit_flair(user[0], flair_text.format(user[1]))

					except Exception as e:
						self.bot.logger.exception("{}".format(datetime.utcnow()))

			removed = self.bot.data.get('removed')
			if removed:
				for name in removed:
					try:
						existing_flair = self.bot.get_flair(name)
						if existing_flair is not None:
							trade_index = existing_flair.find(", Trades:")
							if trade_index != -1:
								flair_text = existing_flair[:trade_index]
								self.bot.set_explicit_flair(name, flair_text)

					except Exception as e:
						self.bot.logger.exception("{}".format(datetime.utcnow()))

		except Exception as e:
			self.bot.logger.exception("{}".format(datetime.utcnow()))

		finally:
			self.bot.data_manager.close()

	def requirements(self):
		return True
