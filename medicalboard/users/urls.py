from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import include, re_path, path


from . import views

app_name = "users"
urlpatterns = [
    re_path('^follow/', login_required(views.FollowView.as_view()), name='follow'),
    re_path(r'^unfollow/(?P<target_id>\d+)/', login_required(views.UnfollowView.as_view()), name='unfollow'),
    re_path('^discover/', login_required(views.DiscoverView.as_view()), name='discover'),
    re_path('^timeline/', login_required(views.TimelineView.as_view()), name='timeline_feed'),
    url(regex=r"^$", view=views.UserListView.as_view(), name="list"),
    url(regex=r"^~redirect/$", view=views.UserRedirectView.as_view(), name="redirect"),
    url(regex=r"^~update/$", view=views.UserUpdateView.as_view(), name="update"),
    url(regex=r"^(?P<username>[\w.@+-]+)/$", view=views.UserDetailView.as_view(), name="detail"),

]
