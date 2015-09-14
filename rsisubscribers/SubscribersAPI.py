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


class SubscribersAPI:
    base_href = "http://sc-api.com/"

    def __init__(self):
        self.data = []

    def send_request(self, request_uri):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, request_uri)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        return buffer.getvalue()

    def find_user(self, subscriber_name):

        """
        Find a subscriber via username
        :param subscriber_name: Name string
        :return string
        """
        request_uri = self.base_href + '?api_source=cache&system=accounts&action=full_profile&target_id=' + subscriber_name
        return self.send_request(request_uri).decode("iso-8859-1")

    def get_all_users(self):
        """
        Find all subscribers
        :return: string
        """
        request_uri = self.base_href + '?api_source=cache&system=accounts&action=all_accounts&ormat=pretty_json'
        return self.send_request(request_uri).decode("iso-8859-1")

    def is_subscriber(self, subscriber_name):
        """
        Detrmines if a user is a subscriber based on username
        :param subscriber_name:
        :return bool:
        """
        try:
            subscriber_info = json.loads(
                self.find_user(subscriber_name),
                object_hook=lambda d: namedtuple(
                    'subscriber_info',
                    d.keys()
                )
                (*d.values())
            )

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

        ]
        try:
            subscriber_info = json.loads(
                self.find_user(subscriber_name),
                object_hook=lambda d: namedtuple(
                    'subscriber_info',
                    d.keys()
                )
                (*d.values())
            )

            """ Handle Uer Not Found """
            if not subscriber_info.data:
                return False

            for org in subscriber_info.data.organizations:
                if org.index('Rank') and high_ranks.index(org['Rank']):
                    return True

        except ValueError:
            return False