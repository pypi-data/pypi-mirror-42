# -*- coding: utf-8 -*-
from django.test import TestCase

from djcms_blog_plugin.models import SimpleBlogEntriesPlugin


class SimpleBlogEntriesPluginTestCase(TestCase):

    def setUp(self):
        pass

    def test_models(self):
        simple_blog_plugin = SimpleBlogEntriesPlugin.objects.create(
            label='Test',
            custom_blog_title='My Blog',
        )
        self.assertEqual("Test", str(simple_blog_plugin))
        self.assertEqual("Test, Simple Blog Plugin", simple_blog_plugin.get_short_description())
