#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks Relating to Auto Posts
~~~~~~~~~~~~~~~
:license: MIT
:author: ste
"""

from Bot.TasksManager import AbstractTaskType
from DataModels.PostsAPI import PostsAPI
import re


class ListPostsTask(AbstractTaskType):
    """
    Sends a list of all current active posts
    """
    api = PostsAPI()

    def handle(self, requirements):
        """
        Check the user is authorised and send the list
        :param requirements:
        :return:
        """
        messages = requirements['messages']

        for message in messages:
            if self.is_mod(message.author):
                all_posts = self.api.get_all_posts()
                self.send_message('list_posts', message.author, all_posts)
            else:
                self.send_message('not_authorised', message.author)
        return True

    def requirements(self):
        """
        Get any messages to the bot which ask for a list
        :return:
        """
        post_messages = self.match_unread('List Posts')
        if post_messages:
            return {'messages': post_messages}
        return False


class CreatePostTask(AbstractTaskType):
    def handle(self, requirements):
        messages = requirements['messages']

        for message in messages:
            post_name = re.sub('Create Post ', '', message.subject)
            body = message.body
            # Todo work out lines
        return True

    def requirements(self):
        create_post_messages = self.match_unread('Create Post')
        if create_post_messages:
            return {'messages': create_post_messages}
        return False


class EditPostTask(AbstractTaskType):
    def handle(self, requirements):
        pass

    def requirements(self):
        pass


class ArchivePostTask(AbstractTaskType):
    def handle(self, requirements):
        pass

    def requirements(self):
        pass


class MakePostTask(AbstractTaskType):
    def handle(self, requirements):
        pass

    def requirements(self):
        pass


class PostponePostTask(AbstractTaskType):
    def handle(self, requirements):
        pass

    def requirements(self):
        pass

class ListLinksInPostTask(AbstractTaskType):
    def handle(self, requirements):
        pass

    def requirements(self):
        pass

class AddLinkToPostTask(AbstractTaskType):
    def handle(self, requirements):
        pass

    def requirements(self):
        pass


class RemoveLinkFromPostTask(AbstractTaskType):
    def handle(self, requirements):
        pass

    def requirements(self):
        pass


class ReorderLinksInPostTask(AbstractTaskType):
    def handle(self, requirements):
        pass

    def requirements(self):
        pass