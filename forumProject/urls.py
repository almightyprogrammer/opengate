"""
URL configuration for forumProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from forumApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('forumApp.urls')),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('accounts/register/', views.register_view, name="register"),
    path('auth1_app/new_post/', views.create_post_view, name="create_post"),
    path('auth1_app/view_posts/', views.post_list_view, name="post_list"),
    path('select2/', include('django_select2.urls')),
]
