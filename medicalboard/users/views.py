from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.views.generic.edit import CreateView, DeleteView, FormView

from stream_django.enrich import Enrich
from stream_django.feed_manager import feed_manager

from .models import User, Follow
from .forms import FollowForm


enricher = Enrich()


Panel = apps.get_model('stream_panel', 'Panel')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ["name"]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class TimelineView(CreateView):
    # might have to move this view to Panels
    fields= ['text']
    model = Panel
    success_url = reverse_lazy('timeline_feed')
    template_name = 'users/stream/timeline.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TimelineView, self).form_valid(form)

    def get_context_data(self, form=None):
        context = super(TimelineView, self).get_context_data()

        feeds = feed_manager.get_news_feeds(self.request.user.id)
        activities = feeds.get('timeline').get()['results']
        enriched_activities = enricher.enrich_activities(activities)

        context['activities'] = enriched_activities
        context['login_user'] = self.request.user
        context['hashtags'] = Hashtag.objects.order_by('-occurrences')

        return context


class FollowView(CreateView):
    form_class = FollowForm
    model = Follow
    success_url = reverse_lazy('timeline_feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FollowView, self).form_valid(form)


class UnfollowView(DeleteView):
    model = Follow
    success_url = reverse_lazy('timeline_feed')

    def get_object(self):
        target_id = self.kwargs['target_id']
        return self.get_queryset().get(target__id=target_id)



class DiscoverView(TemplateView):
    template_name = 'users/streams/follow_form.html'

    def get_context_data(self):
        context = super(DiscoverView, self).get_context_data()

        users = User.objects.order_by('date_joined')[:50]
        following = []
        for i in users:
            if len(i.followers.filter(user=self.request.user.id)) == 0:
                following.append((i, False))
            else:
                following.append((i, True))

        context['users'] = users,
        context['form'] = FollowForm()
        context['login_user'] = self.request.user
        context['following'] = following

        return context
