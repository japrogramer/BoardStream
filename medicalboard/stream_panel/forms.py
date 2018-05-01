from django.apps import apps
from django.forms import ModelForm

Panel = apps.get_model('stream_panel', 'Panel')
Comments = apps.get_model('stream_panel', 'Comments')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Panel
        fields = ('text',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('panel', 'text',)
