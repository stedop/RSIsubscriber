#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Static methods to populate base instances of models.
~~~~~~~~~~~~~~~
MCP
:license: MIT
"""

from DataModels.TradebotModels import Trade, User, UserAudit

class Model(object):

	@staticmethod
	def create_user(name, flair):
		user = User()
		user.user_id = name
		user.title = flair
		user.flair_ind = "1"

		return user

	@staticmethod
	def create_user_audit(user):
		user_audit = UserAudit()
		user_audit.user_id = user.user_id
		user_audit.title = user.title
		user_audit.flair_ind = user.flair_ind
		user_audit.citizen_id = user.citizen_id

		return user_audit
