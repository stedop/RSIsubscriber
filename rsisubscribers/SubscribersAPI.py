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

    def __init__(self):
        self.data = []

    def find_user(self, subscriber_name):

        """Find a subscriber via username
        :param subscriber_name: Name string
        """
        request_url = 'http://sc-api.com/?api_source=cache&system=accounts&action=full_profile&target_id='

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, request_url + subscriber_name)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body.decode("iso-8859-1")

    def is_subscriber(self, subscriber_name):

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

            """
                Want to find Backer in "forum_roles"
            """
            if subscriber_info.data.forum_roles.index('Backer'):
                return True

        except ValueError:
            return False