from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddingServer(forms.Form):
    server_name = forms.CharField()
    os = forms.CharField(label='Operating System')
    cpu_model = forms.CharField()
    memory = forms.CharField()
    disk = forms.CharField()
    status_choice = ('new', 'New - not used'),('broken', "Broken - Having troubles"),('running', 'Running - Having services'),('free', 'Free - not running anything')
    status = forms.ChoiceField(choices=status_choice)
    cpu_graph = forms.CharField()
    memory_graph = forms.CharField()
    disk_graph = forms.CharField()
    
class AddingUser(forms.Form):
    user_name = forms.CharField()
    status_choice = (('developer', 'developer'),('management', 'management'),('administrator', 'administrator'))
    group = forms.ChoiceField(choices=status_choice)
    email = forms.CharField()
    password = forms.CharField()

class ChangePassword(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)
    reenter_password=forms.CharField(widget=forms.PasswordInput)