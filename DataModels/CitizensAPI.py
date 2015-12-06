#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
citizens
~~~~~~~~~~~~~~~
Wrapper for the RSI subs APi
:license: MIT
"""
from io import BytesIO
from collections import namedtuple
from DataModels import CitizenNotFoundException
import re
import json
import pycurl
from logging import getLogger

log = getLogger("TheBot")


class CitizensAPI(object):
    base_href = "http://sc-api.com/"
    searches = {}
    titles = {
        "Civilian": 0,
        "Scout": 1,
        "Mercenary": 2,
        "Bounty Hunter": 4,
        "Colonel": 8,
        "Freelancer": 16,
        "Rear Admiral": 32,
        "Vice Admiral": 64,
        "High Admiral": 128,
        "Grand Admiral": 256,
        "Lt. Commander": 512,
        "Space Marshal": 1024,
        "Wing Commander": 2048,
        "The Completionist": 4096,
    }

    def __init__(self):
        self.data = []

    def send_request(self, request_uri):
        # Hack to work around python 2.4
        request_uri = str(request_uri.encode('utf-8'))
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, request_uri)
        # Another stupid hack
        c.setopt(c.WRITEFUNCTION, buffer.write)
        # c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        value = buffer.getvalue()
        return value

    def find_user(self, citizen_name):

        """
        Find a citizen via username
        :param citizen_name: Name string
        :return string
        """
        if citizen_name not in self.searches.keys():
            request_uri = "{}?api_source=cache&system=accounts&action=full_profile&target_id={}"\
                .format(self.base_href, citizen_name)
            raw_response = self.send_request(request_uri).decode("iso-8859-1")

            data = json.loads(
                raw_response,
                object_hook=lambda d: namedtuple(
                    'citizen_info',
                    d.keys()
                )
                (
                    *d.values()
                 )
            )

            self.searches[citizen_name] = data
            if hasattr(data.request_stats, 'query_status') and data.request_stats.query_status == "failed":
                raise CitizenNotFoundException("Citizen " + citizen_name + " not found")
        return self.searches[citizen_name]

    def is_subscribing(self, citizen_name):
        """
        Determines if a user is a citizen based on username
        :param citizen_name:
        :return bool:
        """

        citizen_info = self.find_user(citizen_name)

        if citizen_info.data.status is "active":
            return True
        return False

    def is_backer(self, citizen_name):
        """
        Determines if the user is a backer
        :param citizen_name:
        :return:
        """
        citizen_info = self.find_user(citizen_name)
        if citizen_info.data.forum_roles.index('Backer'):
            return True
        return False

    def is_high_rank(self, citizen_name):
        """
        Finds out if the user is high rank
        :param citizen_name:
        :return:
        """

        citizen_info = self.find_user(citizen_name)
        rank = citizen_info.data.title
        if self.titles[rank] >= 128:
            return True
        return False

    def get_rank(self, citizen_name):
        citizen_info = self.find_user(citizen_name)
        rank = citizen_info.data.title
        return self.titles[rank]

    def is_authenticated(self, citizen_name, reddit_name):
        """
        Finds authentication Link
        :param citizen_name:
        :param reddit_name:
        :return:
        """

        try:
            citizen_info = self.find_user(citizen_name)
            bio = str(citizen_info.data.bio)

            if re.search(r"reddit.com/u(ser)?/" + reddit_name + "/?\s*(<br />)?\\n", bio, re.IGNORECASE):
                return True
            return False
        except ValueError:
            return False

    def get_title(self, rank):
        for title, level in self.titles.items():
            if level == rank:
                return rank
        return False
