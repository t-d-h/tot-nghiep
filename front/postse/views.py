from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Post

from django.views.generic import ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreatePostForm

class ListPostView(ListView):
  model = Post
  def get (self, request, *args, **kwargs):
    template_name = 'posts/list-posts.html' # sẽ được tạo ở phần dưới
    obj = {
      'posts': Post.objects.all()
    }
    return render(request, template_name, obj)
class CreatePostView(SuccessMessageMixin, CreateView):
  template_name = 'posts/create-post.html'
  form_class = CreatePostForm
  success_message = 'Crate Post successfully!'