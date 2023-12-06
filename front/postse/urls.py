from django.conf.urls import url
from django.contrib import admin
from posts.views import (
  ListPostView,
)

urlpatterns = [
    url(r'^list-posts/$', ListPostView.as_view(), name='list-posts'),
    url(r'^create-post/$', CreatePostView.as_view(), name='create-post'),
]