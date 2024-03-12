"""
URL configuration for tot_nghiep project.

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
from django.urls import path

from servers_management import views, servers_funcs, services_funcs, users_funcs
#
from django.core.exceptions import PermissionDenied
from django.views.defaults import page_not_found
# from servers_management.admin import admin_view
# admin.site.admin_view = admin_view

urlpatterns = [
    path('', views.index, name='home'),
    #path('admine/', admin.site.urls),
    #path(r'^admine/', page_not_found),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('admin/', views.admin_view, name='admin_view'),

    path('users/', users_funcs.users, name='users'),
    path('users/add/', users_funcs.users_add, name='users_add'),
    path("users/detail/<int:user_id>/", users_funcs.users_detail, name="users_detail"),
    path("users/modify/<int:user_id>/", users_funcs.users_modify, name="users_modify"),
    path('users/password/', views.change_password, name='change_password'),

    path("services/detail/<int:service_id>/", services_funcs.service_detail, name="service_detail"),
    path("services/modify/", services_funcs.service_detail, name="service_modify"),
    path('services/add/', services_funcs.service_add, name='service_add'),
    path('services/', services_funcs.services, name='services'),

    path('servers/', servers_funcs.servers, name='servers'),
    path('servers/add/', servers_funcs.servers_add, name='servers_add'),
    path("servers/detail/<int:server_id>/", servers_funcs.server_detail, name="server_detail"),
    path("servers/modify/", servers_funcs.server_detail, name="server_modify"),
    path("servers/monitor/<int:server_id>/", servers_funcs.server_monitor, name="server_monitor")
]
