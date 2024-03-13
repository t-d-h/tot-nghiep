from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader #test
import datetime
from .forms import *
from django.contrib.auth import authenticate, login, logout
from servers_management.models import *

from django import forms 
from django_tables2 import RequestConfig

from django.contrib import messages

# Server table
def servers(request): 
    if request.user.is_authenticated:
        list_user_group = list(request.user.groups.values_list('name',flat = True))
        if request.user.is_superuser:
            table = ServerTable(Servers.objects.all())
            RequestConfig(request).configure(table)
            return render(request, "servers/servers.html", {"table": table, "is_admin": "true"})
        if "management" in list_user_group:
            table = ServerTable(Servers.objects.all())
            table.exclude =('edit_button')
            RequestConfig(request).configure(table)
            return render(request, "servers/servers.html", {"table": table})
    return render(request, '403.html', {})


def servers_add(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = AddingServer(request.POST)
                if form.is_valid():
                    service = Servers(
                        server_name = form.cleaned_data['server_name'],
                        cpu_model = form.cleaned_data['cpu_model'],
                        memory = form.cleaned_data['memory'],
                        os = form.cleaned_data['os'],
                        disk = form.cleaned_data['disk'],
                        status = form.cleaned_data['status'],
                        cpu_graph = form.cleaned_data['cpu_graph'],
                        memory_graph = form.cleaned_data['memory_graph'],
                        disk_graph = form.cleaned_data['disk_graph'],
                    )
                    service.save()
                    return  HttpResponseRedirect("/servers/")
            else:
                form = AddingServer()
            return render(request, "servers/server_add.html", {"form": form})
    return render(request, '403.html', {})

def server_detail(request, server_id=1):
    class ServerDetail(forms.Form):
        # Get current value
        default_server_name = str(list(Servers.objects.values_list('server_name').filter(id=server_id))[0][0])
        default_cpu_model =  str(list(Servers.objects.values_list('cpu_model').filter(id=server_id))[0][0])
        default_memory =  str(list(Servers.objects.values_list('memory').filter(id=server_id))[0][0])
        default_active_service =  str(list(Servers.objects.values_list('active_service').filter(id=server_id))[0][0])
        default_disk =  str(list(Servers.objects.values_list('disk').filter(id=server_id))[0][0])
        default_status =  str(list(Servers.objects.values_list('status').filter(id=server_id))[0][0])
        default_os =  str(list(Servers.objects.values_list('os').filter(id=server_id))[0][0])
        default_cpu_graph = str(list(Servers.objects.values_list('cpu_graph').filter(id=server_id))[0][0])
        default_memory_graph = str(list(Servers.objects.values_list('memory_graph').filter(id=server_id))[0][0])
        default_disk_graph = str(list(Servers.objects.values_list('disk_graph').filter(id=server_id))[0][0])

        # HTML Input fields
        server_id_input = forms.CharField(initial=server_id,widget = forms.HiddenInput())
        server_name = forms.CharField(initial=default_server_name)
        cpu_model = forms.CharField(initial=default_cpu_model)
        memory = forms.CharField(initial=default_memory)
        os = forms.CharField(initial=default_os)
        active_service = forms.CharField(initial=default_active_service,widget = forms.HiddenInput())
        old_server_name=forms.CharField(initial=default_server_name,widget = forms.HiddenInput())
        disk = forms.CharField(initial=default_disk)
        cpu_graph=forms.CharField(initial=default_cpu_graph)
        memory_graph=forms.CharField(initial=default_memory_graph)
        disk_graph=forms.CharField(initial=default_disk_graph)
        status_choice = (('new', 'New - not used'),('broken', "Broken - Can't be used"),('running', 'Running - Having services'),('free', 'Free - not running anything'))
        status = forms.ChoiceField(choices=status_choice,initial=default_status)
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = ServerDetail(request.POST)
                if form.is_valid():
                    server = Servers(
                        id = form.cleaned_data['server_id_input'],
                        server_name = form.cleaned_data['server_name'],
                        cpu_model = form.cleaned_data['cpu_model'],
                        memory = form.cleaned_data['memory'],
                        os = form.cleaned_data['os'],
                        active_service = form.cleaned_data['active_service'],
                        disk = form.cleaned_data['disk'],
                        status = form.cleaned_data['status'],
                        cpu_graph = form.cleaned_data['cpu_graph'],
                        memory_graph = form.cleaned_data['memory_graph'],
                        disk_graph = form.cleaned_data['disk_graph']
                    )
                    server.save()
                    # incase we change server name, we need to reload service table
                    
                    service_list = []
                    for j in list(Services.objects.values_list('id').filter(used_server=form.cleaned_data['old_server_name'])):
                        service_list.append(j[0])
                    for i in service_list:
                        print("effected service: " + str(i))
                        service = Services.objects.get(id=i)
                        service.used_server = form.cleaned_data['server_name']
                        service.save()
                    return  HttpResponseRedirect("/servers/")
            else:
                form = ServerDetail()
                cpu_graphs = str(list(Servers.objects.values_list('cpu_graph').filter(id=server_id))[0][0])
                memory_graphs = str(list(Servers.objects.values_list('memory_graph').filter(id=server_id))[0][0])
                disk_graphs = str(list(Servers.objects.values_list('disk_graph').filter(id=server_id))[0][0])
                context = { "form": form,
                            "cpu_graphs": cpu_graphs, 
                            "memory_graphs": memory_graphs, 
                            "disk_graphs": disk_graphs}

            return render(request, "servers/server_detail.html", context)
    return render(request, '403.html', {})

def server_monitor(request, server_id):
    server_name = str(list(Servers.objects.values_list('server_name').filter(id=server_id))[0][0])
    cpu_graphs = str(list(Servers.objects.values_list('cpu_graph').filter(id=server_id))[0][0])
    memory_graphs = str(list(Servers.objects.values_list('memory_graph').filter(id=server_id))[0][0])
    disk_graphs = str(list(Servers.objects.values_list('disk_graph').filter(id=server_id))[0][0])

    #id = str(list(Servers.objects.values_list('id').filter(id=server_id))[0][0])
    sever_name = str(list(Servers.objects.values_list('server_name').filter(id=server_id))[0][0])
    cpu_model = str(list(Servers.objects.values_list('cpu_model').filter(id=server_id))[0][0])
    memory = str(list(Servers.objects.values_list('memory').filter(id=server_id))[0][0])
    active_service = str(list(Servers.objects.values_list('active_service').filter(id=server_id))[0][0])
    disk = str(list(Servers.objects.values_list('disk').filter(id=server_id))[0][0])
    status = str(list(Servers.objects.values_list('status').filter(id=server_id))[0][0])
    os = str(list(Servers.objects.values_list('os').filter(id=server_id))[0][0])
    
    context = { 
                "id": server_id,
                "server_name": server_name,
                "memory": memory,
                "disk": disk,
                "cpu_model": cpu_model,
                "active_service": active_service,
                "status": status,
                "os": os,
                "cpu_graphs": cpu_graphs, 
                "memory_graphs": memory_graphs, 
                "disk_graphs": disk_graphs}

    return render(request, "servers/servers_monitor.html", context)