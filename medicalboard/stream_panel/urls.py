from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import include, re_path, path


from . import views

app_name = "stream_panel"
urlpatterns = [
    re_path('^add/comments/(?P<panel_id>\d+)', login_required(views.CommentsView.as_view()), name='add_comment'),
]
