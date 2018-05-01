from django.apps import apps
from django.forms import ModelForm

Comments = apps.get_model('stream_panel', 'Comments')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('panel', 'text',)
