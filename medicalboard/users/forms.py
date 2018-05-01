from django.apps import apps
from django import forms
from django.contrib.auth import get_user_model
from .models import Follow


# Follow = apps.get_model('Users', 'Follow')

class FollowForm(forms.ModelForm):

    class Meta:
        exclude = set()
        model = Follow


