from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm, CommentForm, Comment
from .models import Post, Comment
from .forms import PostForm
from django.contrib import messages
import asyncio
from asgiref.sync import sync_to_async


async def register_view(request):
    error_message = ""
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email_address")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            email_exists = await sync_to_async(User.objects.filter(email=email).exists)()
            username_exists = await sync_to_async(User.objects.filter(username=username).exists)()

            if email_exists and username_exists:
                error_message = "Email AND username already exist!"
            elif email_exists:
                error_message = "Email already exists!"
            elif username_exists:
                error_message = "Username already exists!"

            if error_message:
                return render(request, "accounts/register.html", {"form": form, "error": error_message})

            user = await sync_to_async(User.objects.create_user)(username=username, password=password)

            await asyncio.sleep(3)

            await sync_to_async(login)(request, user)

            return redirect("home")

    return render(request, "accounts/register.html", {"form": form, "error": error_message})


async def login_view(request):
    
    error_message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = await sync_to_async(authenticate)(request, username=username, password=password)

        if user is not None:
            await sync_to_async(login)(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            await asyncio.sleep(1)
            return redirect(next_url)
        else:
            await asyncio.sleep(3)
            messages.error(request, "Invalid credentials!")
            return redirect('login')
    
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
            return redirect('post_list')
    
    return render(request, 'auth1_app/new_post.html', {'form':form})

@login_required
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'auth1_app/view_post.html', {"posts": posts})

@login_required
def post_view(request, id):
    # Show the post and all comments
    post = get_object_or_404(Post, post_id=id)
    comments = post.comments.filter(parent__isnull=True)
    form = CommentForm()
    return render(request, 'auth1_app/view_individual_post.html', {
        'post': post,
        'comment_form': form,
        'comments': comments,
    })
#Protected View

@login_required
def edit_post_view(request, id):
    post = get_object_or_404(Post, post_id=id)

    # Prevent users who are not the author from editing
    if request.user != post.author:
        return render(request, 'auth1_app/view_individual_post.html', {
            'post': post,
            'error': "You are not allowed to edit this post!"
        })
    # Preload post content
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('individual_post', id=post.post_id)  # Redirect to the post view

    return render(request, 'auth1_app/edit_post.html', {'form': form, 'post': post})

@login_required
def edit_comment_view(request, post_id, id):
    comment = get_object_or_404(Comment, id=id)
    post = comment.post
    # Prevent users who are not the author from editing
    if request.user != comment.user:
        return render(request, 'auth1_app/view_individual_post.html', {
            'comment': comment,
            'post' : post,
            'error': "You are not allowed to edit this comment!"
        })
    # Preload comment content
    form = CommentForm(instance=comment)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('individual_post', id=post.post_id)
        
    return render(request, 'auth1_app/edit_comment.html', {'form': form, 'comment': comment, 'post': post})

@login_required
def delete_comment_view(request, post_id, id):
    comment = get_object_or_404(Comment, id=id)
    post = comment.post
    if request.method == "POST":
        if request.user != comment.user:
            return render(request, 'auth1_app/view_individual_post.html', {
                'comment': comment,
                'post' : post,
                'error': "You are not allowed to delete this comment!"
            })
        
        comment.delete()
        return redirect('individual_post', id=comment.post.post_id)

    return render(request, 'auth1_app/delete_comment.html', {'comment': comment, 'post': post})

@login_required
def delete_post_view(request, id):
    post = get_object_or_404(Post, post_id=id)

    if request.method == "POST":
        if request.user != post.author:
            return render(request, 'auth1_app/view_individual_post.html', {
                'post': post,
                'error': "You are not allowed to delete this post!"
            })
        
        post.delete()
        return redirect('post_list')

    return render(request, 'auth1_app/delete_post.html', {'post': post})

MAX_NESTING_DEPTH = 4
@login_required
def post_detail(request, post_id):
    post = Post.objects.get(post_id=post_id)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_id = comment_form.cleaned_data.get('parent_id')
            content = comment_form.cleaned_data.get('content')

            new_comment = Comment(
                post=post,
                user=request.user,
                content=content
            )
            if parent_id:
                parent_comment = Comment.objects.get(comment_id=parent_id)
                new_comment.depth = parent_comment.depth + 1
                if new_comment.depth > MAX_NESTING_DEPTH:
                    return render(request, 'auth1_app/view_individual_post.html', {
                        'post': post,
                        'error': "The comment thread has reached the maximum depth!"
                    })
                new_comment.parent = parent_comment
            new_comment.save()
            return redirect('individual_post', id=post.post_id)
    else:
        comment_form = CommentForm()

    top_level_comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_at')
    context = {
        'post': post,
        'comment_form': comment_form,
        'top_level_comments': top_level_comments,
        'MAX_NESTING_DEPTH': MAX_NESTING_DEPTH
    }
    return render(request, 'auth1_app/view_individual_post.html', context)


class ProtectedView(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'registration/protected.html')
    

