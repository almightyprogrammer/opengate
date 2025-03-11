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
    path('view_post/<int:id>/', views.post_view, name="individual_post"),
    path('edit_post/<int:id>/', views.edit_post_view, name="edit_post"),
    path('delete_post/<int:id>/', views.delete_post_view, name="delete_post"),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit_comment/<int:id>', views.edit_comment_view, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:id>', views.delete_comment_view, name='delete_comment'),
]
