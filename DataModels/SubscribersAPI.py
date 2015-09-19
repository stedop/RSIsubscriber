#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Subscribers
~~~~~~~~~~~~~~~
Wrapper for the RSI subs APi
:license: MIT
"""

import pycurl
from io import BytesIO
import json
from collections import namedtuple
import re

class SubscribersAPI:
    base_href = "http://sc-api.com/"
    searches = {}

    def __init__(self):
        self.data = []

    def send_request(self, request_uri):
        # Hack to work around python 2.4
        # request_uri = str(request_uri.encode('utf-8'))
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, request_uri)
        # Another stupid hack
        # c.setopt(c.WRITEFUNCTION, buffer.write)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        value = buffer.getvalue()
        return value

    def find_user(self, subscriber_name):

        """
        Find a subscriber via username
        :param subscriber_name: Name string
        :return string
        """
        if subscriber_name not in self.searches.keys():
            request_uri = "{}?api_source=cache&system=accounts&action=full_profile&target_id={}"\
                .format(self.base_href, subscriber_name)
            raw_response = self.send_request(request_uri).decode("iso-8859-1")
            self.searches[subscriber_name] = json.loads(
                raw_response,
                object_hook=lambda d: namedtuple(
                    'subscriber_info',
                    d.keys()
                )
                (*d.values())
            )

        return self.searches[subscriber_name]

    def is_subscriber(self, subscriber_name):
        """
        Detrmines if a user is a subscriber based on username
        :param subscriber_name:
        :return bool:
        """
        try:
            subscriber_info = self.find_user(subscriber_name)
            """ Handle Uer Not Found """
            if not subscriber_info.data:
                return False

            if subscriber_info.data.forum_roles.index('Backer'):
                return True

        except ValueError:
            return False

    def is_high_rank(self, subscriber_name):
        """
        Finds out if the user is high rank
        :param subscriber_name:
        :return:
        """
        high_ranks = [
            'High Admiral',
            'Grand Admiral',
            'Lt. Commander',
            'Space Marshall',
            'Wing Commander',
            'Completionist'
        ]
        try:
            subscriber_info = self.find_user(subscriber_name)

            """ Handle Uer Not Found """
            if not subscriber_info.data:
                return False

            for org in subscriber_info.data.organizations:
                if org.index('Rank') and high_ranks.index(org['Rank']):
                    return True

        except ValueError:
            return False

    def is_authenticated(self, subscriber_name):
        """
        Finds authentication Link
        :param subscriber_name:
        :return:
        """
        try:
            subscriber_info = self.find_user(subscriber_name)
            link = "http://www.reddit.com/user/" + subscriber_name
            link = re.escape(link)
            bio = str(subscriber_info.data.bio)
            """ Handle Uer Not Found """
            if not subscriber_info.data:
                return False

            if bio.find(link):
                return True
        except ValueError:
            return False