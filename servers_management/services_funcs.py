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
from django.contrib.auth import get_user_model

# get server id of a service or from server's name
def get_server_id(input, input_type):
    server_id = ""

    if input_type == "service_id":
        server_id =  str(list(Service_mapping2.objects.values_list('server_id').filter(id=input))[0][0])
    
    if input_type == "server_name":
        server_id =  str(list(Servers.objects.values_list('id').filter(server_name=input))[0][0])

    print("This is the new server id: " + str(server_id))
    return server_id

def update_service_list(server_id):

    server = Servers.objects.get(id=server_id)
    server.active_service = "None"
    server.save()

    active_service_ids_of_server = list(Service_mapping2.objects.values_list('id').filter(server_id=server_id))

    active_service_id = []
    for i in active_service_ids_of_server:
        active_service_id.append(i[0])

    active_service_name_string = []
    for j in active_service_id:
        service_name = Services.objects.values_list('service_name').filter(id=j)
        active_service_name_string.append(list(service_name)[0][0])

    final_service_names = ', '.join(active_service_name_string)

    server = Servers.objects.get(id=server_id)
    server.active_service = final_service_names
    server.status= "running"
    server.save()

def service_add(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            class AddingService(forms.Form):
                Servers = Servers.objects.values_list('server_name').exclude(status='broken')
                server_names = []
                for i in list(Servers):
                    dst_tuple = (i[0], i[0])
                    server_names.append(dst_tuple) # [('front2', 'front2'), ('front3v', 'front3v'),]
                user_list = []
                for i in list(get_user_model().objects.all()):
                    dst_tuple = (i.username, i.username)
                    user_list.append(dst_tuple)
                service_name = forms.CharField()
                requested_server = forms.CharField(label='Server: ', widget=forms.Select(choices=server_names))
                owner = forms.CharField(widget=forms.Select(choices=user_list))
            if request.method == 'POST':
                form = AddingService(request.POST)
                if form.is_valid():
                    # save to service table
                    service = Services(
                        owner = form.cleaned_data['owner'], 
                        service_name = form.cleaned_data['service_name'],
                        used_server = form.cleaned_data['requested_server'],
                    )
                    service.save()

                    # save to mapping table (new)
                    server_id = str(list(Servers.objects.values_list('id').filter(server_name=form.cleaned_data['requested_server']))[0][0])
                    service_id = str(list(Services.objects.values_list('id').filter(service_name=form.cleaned_data['service_name']))[0][0])

                    service_mapping2 = Service_mapping2(
                        server_id = server_id,
                        id = service_id
                    )
                    service_mapping2.save()

                    update_service_list(server_id)
                    #active_service_name = 
                    return HttpResponseRedirect("/services/")
            else:
                form = AddingService()
            return render(request, "services/service_add.html", {"form": form})
        return render(request, '403.html', {})
    return redirect('/login')
##################################

def service_detail(request, service_id=0):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            class ServiceDetail(forms.Form):
                if request.method == 'GET':
                    default_service_name = str(list(Services.objects.values_list('service_name').filter(id=service_id))[0][0])
                    default_used_server =  str(list(Services.objects.values_list('used_server').filter(id=service_id))[0][0])
                    default_owner =  str(list(Services.objects.values_list('owner').filter(id=service_id))[0][0])
                    Servers = Servers.objects.values_list('server_name').exclude(status='broken')
                    server_names = []
                    for i in list(Servers):
                        dst_tuple = (i[0], i[0])
                        server_names.append(dst_tuple) # [('front2', 'front2'), ('front3v', 'front3v'),]

                    user_list = []
                    for i in list(get_user_model().objects.all()):
                        dst_tuple = (i.username, i.username)
                        user_list.append(dst_tuple)
                    
                    # HTML Input fields
                    service_id_input = forms.CharField(initial=service_id,widget = forms.HiddenInput())
                    service_name = forms.CharField(initial=default_service_name)
                    used_server = forms.CharField(label='Server: ', widget=forms.Select(choices=server_names), initial=default_used_server)
                    owner = forms.CharField(initial=default_owner,  widget=forms.Select(choices=user_list))
                    remove = forms.BooleanField(required = False)
                    old_server_name = forms.BooleanField(initial=default_used_server,widget = forms.HiddenInput())
                elif request.method == 'POST':
                    service_id_input = forms.CharField(widget = forms.HiddenInput())
                    service_name = forms.CharField()
                    used_server = forms.CharField(label='Server: ')
                    owner = forms.CharField()
                    remove = forms.BooleanField(required = False)
                    old_server_name = forms.CharField()
            if request.method == 'POST':
                form = ServiceDetail(request.POST)
                if form.is_valid():
                    service = Services(
                        id = form.cleaned_data['service_id_input'],
                        service_name = form.cleaned_data['service_name'],
                        used_server = form.cleaned_data['used_server'],
                        owner = form.cleaned_data['owner'],
                    )
                    if form.cleaned_data['remove'] != True:
                        server_id =  str(list(Servers.objects.values_list('id').filter(server_name=request.POST['used_server']))[0][0])
                        service_id = str(request.POST['service_id_input'])

                        service_mapping2 = Service_mapping2(
                            server_id = server_id,
                            id = service_id
                        )
                        service_mapping2.save()

                        service.save()
                        update_service_list(server_id)
                        update_service_list(get_server_id(form.cleaned_data['old_server_name'], "server_name"))
                    else:
                        Service_mapping2.objects.filter(id=form.cleaned_data['service_id_input']).delete()
                        update_service_list(get_server_id(form.cleaned_data['old_server_name'], "server_name"))
                        service.delete()

                    #update_service_list(get_server_id(str(form.cleaned_data['service_id_input']), "service_id"))
                    return  HttpResponseRedirect("/services/")
            else:
                form = ServiceDetail()
            return render(request, "services/service_detail.html", {"form": form})
        return render(request, '403.html', {})
    return redirect('/login')
# Admin's adding server page

# service table 

def services(request):
    if request.user.is_authenticated:
        list_user_group = list(request.user.groups.values_list('name',flat = True))
        
        if request.user.is_superuser:
            table = ServiceTable(Services.objects.all())
            RequestConfig(request).configure(table)
            return render(request, "services/services.html", {"table": table, "is_admin": "true"})


        if "management" in list_user_group:
            table = ServiceTable(Services.objects.all()) # where owner = logged in username
            table.exclude =('edit_button')
            RequestConfig(request).configure(table)
            return render(request, "services/services.html", {"table": table})

        if "developer" in list_user_group:
            table = ServiceTable(Services.objects.filter(owner=request.user.username))
            table.exclude =('edit_button')
            RequestConfig(request).configure(table)
            return render(request, "services/services.html", {"table": table})
    return redirect('/login')