# -*- coding: utf-8 -*-
from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from djcms_blog.models import Blog, BlogTitle, Post, PostTitle, Tag, Author

from djcms_blog_plugin.cms_plugins import SimpleBlogEntriesPluginCMS


class SimpleBlogEntriesPluginTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user("carlosmart", "me@carlosmart.co", "123123")
        self.user.first_name = "Carlos"
        self.user.last_name = "Martinez"
        self.author = Author.objects.create(
            user=self.user,
            cover="author-cover.jpg",
            image="author-image.jpg",
            slug="carlosmart",
            location="Colombia",
            website="https://carlosmart.co",
            facebook_profile="https://facebook.com/carlosmart626",
            twitter_profile="https://twitter.com/carlosmart626",
            block_header="",
            block_footer=""
        )
        self.blog = Blog.objects.create(
            title="My Blog",
            slug="my-blog",
            cover="cover.jpg",
            block_header="",
            block_footer=""
        )
        self.blog_title = BlogTitle.objects.create(
            blog=self.blog,
            language="en",
            title="My blog",
            description="My blog description",
        )
        self.tag = Tag.objects.create(
            blog=self.blog,
            cover="tag_cover.jpg",
            name="My Tag",
            slug="my-tag",
            color="blue",
        )
        self.post_1 = Post.objects.create(
            blog=self.blog,
            title="My post",
            slug="my-post",
            author=self.author,
        )
        self.post_1_title = PostTitle.objects.create(
            post=self.post_1,
            title="My post",
            language="en",
            description="My post description",
            body="My post body",
            publisher_is_draft=False,
            published=True
        )
        self.post_2 = Post.objects.create(
            blog=self.blog,
            title="My post 2",
            slug="my-post 2",
            author=self.author,
        )
        self.post_2_title = PostTitle.objects.create(
            post=self.post_2,
            title="My post 2",
            language="en",
            description="My post 2 description",
            body="My post 2 body",
            publisher_is_draft=False,
            published=True
        )

    def test_models(self):
        simple_blog_plugin_simple_cms = SimpleBlogEntriesPluginCMS()
        self.assertIsNotNone(simple_blog_plugin_simple_cms)
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            SimpleBlogEntriesPluginCMS,
            'en',
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        self.assertIn("My post", html)
        self.assertIn("My post description", html)
        self.assertIn("My post 2", html)
        self.assertIn("My post 2 description", html)
        self.assertIn("carlosmart", html)
        self.assertIn("My blog", html)

        model_instance = add_plugin(
            placeholder,
            SimpleBlogEntriesPluginCMS,
            'en',
        )
        model_instance.custom_blog_title = "This is my new blog"
        model_instance.save()
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        self.assertIn("My post", html)
        self.assertIn("My post description", html)
        self.assertIn("My post 2", html)
        self.assertIn("My post 2 description", html)
        self.assertIn("carlosmart", html)
        self.assertIn("This is my new blog", html)
