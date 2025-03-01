from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Post
from .forms import PostForm


# Create your views here.

def register_view(request):
    
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'accounts/register.html', {'form':form})    



def login_view(request):
    error_message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Invalid credentials!"
    
    return render(request, 'accounts/login.html', {'error': error_message})


def logout_view(request):
    
    if request.method == "POST":
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
    






def home_view(request):
    
    return render(request, 'auth1_app/home.html')


@login_required
def create_post_view(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    
    return render(request, 'auth1_app/new_post.html', {'form':form})

@login_required
def post_list_view(request):
    posts = Post.objects.all()
    return render(request, 'auth1_app/view_post.html', {"posts": posts})

def post_view(request, id):
    post = Post.objects.get(post_id=id)
    return render(request, 'auth1_app/view_individual_post.html', {'post':post})
    
#Protected View


class ProtectedView(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'registration/protected.html')
    

