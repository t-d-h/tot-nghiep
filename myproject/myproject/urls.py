"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from myapp import views
#
from django.core.exceptions import PermissionDenied
from django.views.defaults import page_not_found
from myapp.admin import admin_view
admin.site.admin_view = admin_view
#
urlpatterns = [
    #path khong co regex con re_path thi co
    path('', views.index, name='home'),
    path('users/', admin.site.urls),
    path(r'^users/', page_not_found),
    #path(r'^acmin/', include(admin.site.urls)),
    path('hello/', views.hello, name='hello'),
    path('helloa/', views.helloa, name='helloa'),
    path('param/', views.param, name='param'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin/', views.admin_view, name='admin_view'),

    # url parameter
    path("articles/<int:articleId>/", views.viewArticle),
    # path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail year,mounth,slug la var truyen vao func

    # re_path(r'^myapp/', include('myapp.urls')),
    # path('',include('myapp.urls'))
]
