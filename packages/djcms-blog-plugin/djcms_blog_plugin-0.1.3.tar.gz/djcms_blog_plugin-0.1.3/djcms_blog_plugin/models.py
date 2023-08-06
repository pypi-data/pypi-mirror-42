from cms.models import CMSPlugin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class SimpleBlogEntriesPlugin(CMSPlugin):
    """
    Segment
    """
    label = models.CharField(
        verbose_name=_('Label'),
        blank=True,
        max_length=255,
        help_text=_('Overrides the display name in the structure mode.'),
    )
    custom_blog_title = models.CharField(
        verbose_name=_('Custom Title'),
        blank=True,
        max_length=255,
        help_text=_('Overrides the display name in the widget.'),
    )
    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.label

    def get_short_description(self):
        return "{}, Simple Blog Plugin".format(self.label)
