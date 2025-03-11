from django.urls import path
from . import views



urlpatterns = [
    path('', views.home_view, name="home"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('protected/', views.ProtectedView.as_view(), name="protected"),
    path('new_post/', views.create_post_view, name="create_post"),
    path('view_posts/', views.post_list_view, name="post_list"),
    path('view_post/<int:id>/', views.post_view, name="individual_post")

]
