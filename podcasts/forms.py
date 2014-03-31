from django import forms
from django.forms.util import ErrorDict
from django.forms.forms import NON_FIELD_ERRORS


class AddPodcastForm1(forms.Form):
    feed = forms.URLField(label='RSS or Atom feed',
                          help_text='Address to the podcast\'s RSS or Atom ' +
                                    'feed.')

    # Will be implemented in Django 1.7: https://docs.djangoproject.com/en/dev/ref/forms/api/#django.forms.Form.add_error
    # Implementation below based on: http://stackoverflow.com/a/5719573/595990
    def add_error(self, field, error):
        if not self._errors:
            self._errors = ErrorDict()
        if not field:
            field = NON_FIELD_ERRORS
        if not field in self._errors:
            self._errors[field] = self.error_class()
        self._errors[field].append(error)
        pass


class AddPodcastForm2(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    link = forms.URLField(label='Address to homepage', widget=forms.TextInput(
        attrs={'readonly': 'readonly'}), required=False)
    description = forms.CharField(label='Short summary', widget=forms.Textarea(
        attrs={'readonly': 'readonly', 'rows': 5}), required=False)
