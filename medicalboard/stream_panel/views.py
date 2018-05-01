from django.apps import apps
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView

from stream_django.enrich import Enrich
from stream_django.feed_manager import feed_manager


enricher = Enrich()


Panel = apps.get_model('stream_panel', 'Panel')
Comments = apps.get_model('stream_panel', 'Comments')


class PanelView(CreateView):
    fields= ['text']
    model = Panel
    success_url = reverse_lazy('users:timeline_feed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CommentsView, self).form_valid(form)


class CommentsView(CreateView):
    fields= ['text']
    model = Comments
    success_url = reverse_lazy('users:timeline_feed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.panel = self.kwargs['panel_id']
        return super(CommentsView, self).form_valid(form)
