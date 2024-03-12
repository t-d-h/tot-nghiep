from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .forms import UserCreationForm, LoginForm

from django.contrib.auth import authenticate, login, logout 



def hello(request):
   return render(request, "hello.html", {})

def helloa(request, number=1):
   text = "<h1>welcome to my app number %s!</h1>"% number
   return HttpResponse(text)

# url parameter
def viewArticle(request, articleId):
   text = "Displaying article Number : %s"%articleId
   return HttpResponse(text)

# htlml parameter
def param(request):
   today = datetime.datetime.now().date()
   return render(request, "html-parameter.html", {"today" : today})





# web here  
def index(request):

   user_group = request.user.groups.values_list('name',flat = True)
   print(user_group)
   if 'admin' in list(user_group):
      return render(request, 'admin_view.html', {'msg': 'this is mgs'})
   #return render(request, 'index.html')
   return redirect('/login')

#authen
def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

# login page
def user_login(request):
   if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']
         user = authenticate(request, username=username, password=password)
         if user and username == 'root':  
               login(request, user)
               return redirect('/users')
         if user:
               login(request, user)    
               return redirect('home')
   else:
      form = LoginForm()
      return render(request, 'login.html', {'form': form})
   return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
   logout(request)
   return redirect('login')

# admin view:
def admin_view(request):
   user_group = request.user.groups.values_list('name',flat = True)
   print(user_group)
   if 'admin' in list(user_group):
      return render(request, 'admin_view.html', {'msg': 'this is mgs'})
   return HttpResponse("you are not admin, redirecting")
