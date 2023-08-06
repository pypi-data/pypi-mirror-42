from django import forms

from .models import SimpleBlogEntriesPlugin


class SimpleBlogEntriesPluginForm(forms.ModelForm):

    class Meta:
        model = SimpleBlogEntriesPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
