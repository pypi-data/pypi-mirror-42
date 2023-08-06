from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from djcms_blog.models import Blog

from .forms import SimpleBlogEntriesPluginForm
from .models import SimpleBlogEntriesPlugin


class SimpleBlogEntriesPluginCMS(CMSPluginBase):
    model = SimpleBlogEntriesPlugin
    module = _("Django CMS Blog")
    name = _('Simple Blog Entries Plugin')
    render_template = "djcms_blog_plugin/simple_blog_entries.html"
    allow_children = False
    form = SimpleBlogEntriesPluginForm
    language = None

    def render(self, context, instance, placeholder):
        self.language = translation.get_language()
        context = super(SimpleBlogEntriesPluginCMS, self).render(context, instance, placeholder)
        blog = Blog.objects.get(pk=settings.DJCMS_BLOG_ID)
        blog_lang_object = blog.get_language_object(self.language)
        instance.get_posts = list(blog.get_posts())[:settings.DJCMS_BLOG_ENTRIES_NUMBER]
        instance.title = instance.custom_blog_title or blog_lang_object.title
        for post in instance.get_posts:
            post_object = post.language_object(self.language)
            post.title = post_object.title
            post.description = post_object.description
            post.published_date = post_object.published_date
        return context


plugin_pool.register_plugin(SimpleBlogEntriesPluginCMS)
