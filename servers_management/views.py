from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader #test
import datetime, os
from .forms import *
from django.contrib.auth import authenticate, login, logout 
from servers_management.models import *
from django import forms 
from django_tables2 import RequestConfig

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import django_tables2 as tables
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    list_user_group = list(request.user.groups.values_list('name',flat = True))
    if request.user.is_authenticated:
        total_number_of_servers = Servers.objects.all().count()
        total_number_of_running_servers = Servers.objects.exclude(status='broken').count()
        total_number_of_broken_servers = Servers.objects.filter(status='broken').count()
        total_number_of_free_servers = Servers.objects.filter(status='free').count()
        total_number_of_new_servers = Servers.objects.filter(status='new').count()
        total_number_of_services = Services.objects.all().count()
        if request.user.is_superuser:
            server_table = ServerTable(Servers.objects.all())
            server_table.exclude =('active_service', 'edit_button', 'monitor_button')
            RequestConfig(request).configure(server_table)
            cpu_graph = os.environ['CPU_GRAPH']
            mem_graph = os.environ['MEMORY_GRAPH']
            disk_graph = os.environ['DISK_GRAPH']
            return render(request, 'views/admin_view.html', {"server_table": server_table, 
                "cpu_graph": cpu_graph,
                "mem_graph" : mem_graph,
                "disk_graph" : disk_graph,
                "total_number_of_servers": total_number_of_servers,
                "total_number_of_running_servers": total_number_of_running_servers,
                "total_number_of_broken_servers": total_number_of_broken_servers,
                "total_number_of_new_servers": total_number_of_new_servers,
                "total_number_of_free_servers": total_number_of_free_servers})

        if "management" in list_user_group:
            server_table = ServerTable(Servers.objects.all())
            server_table.exclude =('os', 'id', 'active_service', 'edit_button')
            RequestConfig(request).configure(server_table)
            service_table = ServiceTable(Services.objects.all())
            service_table.exclude =('owner', 'edit_button')
            RequestConfig(request).configure(service_table)
            return render(request, 'views/management_view.html', {"server_table": server_table, 
                "service_table": service_table,
                "total_number_of_servers": total_number_of_servers,
                "total_number_of_running_servers": total_number_of_running_servers,
                "total_number_of_broken_servers": total_number_of_broken_servers,
                "total_number_of_free_servers": total_number_of_free_servers,
                "total_number_of_new_servers": total_number_of_new_servers,
                "total_number_of_services": total_number_of_services})

        if "developer" in list_user_group:
            service_table = ServiceTable(Services.objects.filter(owner=request.user.username))
            service_table.exclude =('edit_button')
            RequestConfig(request).configure(service_table)
            server_list = []
            for j in list(Services.objects.values_list('used_server').filter(owner=request.user.username)):
                server_list.append(j[0])
            server_table = ServerTable(Servers.objects.filter(server_name__in=server_list))
            server_table.exclude =('os', 'id', 'active_service', 'edit_button', 'status')
            RequestConfig(request).configure(server_table)
            total_number_of_services = Services.objects.filter(owner=request.user.username).count()
            total_number_of_running_servers = Services.objects.values_list('used_server').filter(owner=request.user.username).count()
            return render(request, 'views/developer_view.html', {"server_table": server_table, 
                "service_table": service_table,
                "total_number_of_services": total_number_of_services,
                "total_number_of_running_servers": total_number_of_running_servers})
    return redirect('/login')

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
            else:
                messages.error(request, 'Username or password is incorrect.')
                return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'views/login.html', {'form': form})
    return render(request, 'views/login.html', {'form': form})

def user_logout(request):
   logout(request)
   return redirect('login')

def change_password(request):
    if request.method=='POST':
        form=ChangePassword(request.POST)
        if form.is_valid():
            user=User.objects.get(username=request.user.username)
            password = form.cleaned_data['new_password']
            if form.cleaned_data['new_password'] != form.cleaned_data['reenter_password']:
                messages.error(request, 'New password and re-enter password do not match.')
                return redirect('change_password')
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password was successfully updated! Please login again.')
                return redirect('login')
            else:
                messages.error(request, 'Your current password is incorrect.')
                return redirect('change_password')
            
    else:
        form = ChangePassword()
    return render(request, "views/change_password.html", {"form": form})
