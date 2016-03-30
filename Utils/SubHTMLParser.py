#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from HTMLParser import HTMLParser

class SubHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.capture_data = False
		self.uee_tag = False
		self.citizen_number = 0
	
	def handle__starttag(self,  tag,  attrs):
		pass
	
	def handle_endtag(self,  tag):
		pass
	
	"""
	This is kind of weird. The parser reads in the tags that define the 'UEE Citizen Record String', but the next set of data is blank.
	It's the data after that blank one that actually contains the citizen_id we want - hence the use of a boolean that sets a boolean to
	indicate the 'second' pass through.
	"""
	def handle_data(self,  data):
		if self.capture_data:
			# Substring removes the '#' in front of the Citizen ID number.
			self.citizen_number = data[1:]
			self.capture_data = False
		if self.uee_tag:
			self.capture_data = True
			self.uee_tag = False
		elif data == "UEE Citizen Record":
			self.uee_tag = True
		else:
			pass
	
