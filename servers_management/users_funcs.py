from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader #test
import datetime
from .forms import *
from django.contrib.auth import authenticate, login, logout 

from servers_management.models import *

from django import forms 
from django_tables2 import RequestConfig

# user management 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import django_tables2 as tables
from django.contrib.auth.models import User

from django.contrib import messages


# User table
def users(request):
    if request.user.is_authenticated:
        list_user_group = list(request.user.groups.values_list('name',flat = True))
        data = []
        for i in list(User.objects.all()):
            user = {}
            user['name'] = str(i)
            user['id'] = str(i.id)
            user['email'] = str(i.email)
            if str(i.last_login) != 'None':
                user['last_login'] = str(i.last_login.strftime("%c"))
            #query_set = Group.objects.filter(name = str(i))
            query_set=i.groups.all()
            for g in query_set:
                user['group'] = str(g)

            if i.is_superuser:
                user['group'] = "admin"
                user['is_admin'] = "true"
            else:
                user['is_admin'] = "false"
            user['id'] = str(i.id)

            if i.is_active:
                user['is_active'] = "true"
            else:
                user['is_active'] = "false"
            data.append(user)
        class NameTable(tables.Table):
            id = tables.Column()
            name = tables.Column()
            email = tables.Column()
            group = tables.Column()
            is_admin = tables.Column()
            is_active = tables.Column()
            last_login= tables.Column()

            edit_button =  tables.TemplateColumn('<a href="{% url "users_detail" record.id %}" class="btn btn-primary">Edit</a>', verbose_name='', )
            class Meta:
                template_name = "django_tables2/bootstrap.html"

        table = NameTable(data)
        if request.user.is_superuser:
            return render(request, 'users/users.html', {"table": table, "is_admin": "true"})
        if "management" in list_user_group:
            table.exclude = [ 'edit_button', 'is_admin']
            return render(request, 'users/users.html', {"table": table})
        return render(request, '403.html', {})
    return redirect('/login')

def users_add(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = AddingUser(request.POST)
                if form.is_valid():
                    if User.objects.filter(username=form.cleaned_data['user_name']).exists():

                        messages.error(request, 'Username exists')
                        return redirect('users_add')

                    if form.cleaned_data['group'] == "administrator":
                        User.objects.create_superuser(username=form.cleaned_data['user_name'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'])
                    else:
                        User.objects.create_user(username=form.cleaned_data['user_name'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'])
                        user = User.objects.get(username=form.cleaned_data['user_name'])
                        group = Group.objects.get(name=form.cleaned_data['group'])
                        group.user_set.add(user)
                    return  HttpResponseRedirect("/users/")
            else:
                form = AddingUser()
                return render(request, "users/users_add.html", {"form": form})
        return render(request, '403.html', {})
    return redirect('/login')
    
def users_detail(request, user_id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            class UserDetail(forms.Form):
                # Get current value
                user = User.objects.get(id=user_id)
                groups = [("developer", "developer"), ("manager","manager"), ("admin", "admin") ]
                # HTML Input fields
                
                username = forms.CharField(initial=user)
                email = forms.CharField(initial=user.email)
                group = forms.CharField(label='Group:  ', widget=forms.Select(choices=groups))
                new_password = forms.CharField(required = False)
                is_active = forms.BooleanField(initial=user.is_active,required = False)
                #is_superuser = forms.BooleanField(initial=user.is_superuser,required = False)
                remove = forms.BooleanField(required = False)
            if request.method != 'GET':
                return  HttpResponseRedirect("/users/")
            form = UserDetail()
            return render(request, "users/users_detail.html", {"form": form, "user_id": user_id})
        return render(request, '403.html', {})
    return redirect('/login')

def users_modify(request, user_id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            class UserDetail(forms.Form):
                # Get current value
                user = User.objects.get(id=user_id)
                groups = [("admin", "admin"), ("developer", "developer"), ("manager","manager")]
                # HTML Input fields
                username = forms.CharField(initial=user)
                email = forms.CharField(initial=user.email)
                group = forms.CharField(label='Group:  ', widget=forms.Select(choices=groups))
                new_password = forms.CharField(required = False)
                is_active = forms.BooleanField(initial=user.is_active,required = False)
                #is_superuser = forms.BooleanField(initial=user.is_superuser,required = False)
                remove = forms.BooleanField(required = False)
            if request.method == 'POST':
                form = UserDetail(request.POST)
                if form.is_valid():
                    # new email
                    user = User.objects.get(username=form.cleaned_data['username'])
                    user.email = form.cleaned_data['email']
                    user.save()

                    # new group 
                    try:
                        for g in user.groups.all():
                            g.user_set.remove(user)
                    except: 
                        pass
                    
                    if form.cleaned_data['group'] == "admin":
                        user.is_superuser = True
                        user.save()
                    else:
                        user.is_superuser = False
                        user.save()
                        new_group = Group.objects.get(name=form.cleaned_data['group'])
                        new_group.user_set.add(user)

                    # new password if input is not null
                    if form.cleaned_data['new_password'] != "":
                        user.set_password(form.cleaned_data['new_password'])
                        user.save()
                    
                    # active or deactivate
                    if form.cleaned_data['is_active'] == False:
                        user.is_active = False
                        user.save()
                    else:
                        user.is_active = True
                        user.save()

                    # remove user
                    if form.cleaned_data['remove']:
                        user.delete()

            return HttpResponseRedirect("/users/")
        return render(request, '403.html', {})    
    return redirect('/login')