#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks Relating to Auto Posts
~~~~~~~~~~~~~~~
:license: MIT
:author: ste
"""

from Bot import AbstractTaskType
from DataModels import PostModel
import re


class ListPostsTask(AbstractTaskType):
    """
    Sends a list of all current active posts
    """

    def handle(self, requirements):
        """
        Check the user is authorised and send the list
        :param requirements:
        :return:
        """
        messages = requirements['messages']
        for message in messages:
            if self.bot.is_mod(message.author):
                all_posts = self.bot.data_manager.query(PostModel).filter(PostModel.archived == 0).all()
                self.bot.logger.debug(all_posts)
                self.bot.logger.debug(len(all_posts))
                if (len(all_posts) > 0):
                    self.bot.send_message('list_posts', message.author, all_posts)
                else:
                    self.bot.send_message('no_posts', message.author, all_posts)
            else:
                self.bot.send_message('not_authorised', message.author)
        return True

    def requirements(self):
        """
        Get any messages to the bot which ask for a list
        :return:
        """
        post_messages = self.bot.match_unread('List Posts')
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
        create_post_messages = self.bot.match_unread('Create Post')
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