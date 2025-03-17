from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


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
    path('posts/<int:post_id>/edit_comment/<int:id>/', views.edit_comment_view, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:id>/', views.delete_comment_view, name='delete_comment'),
    path('view_industry_posts/<str:industry>/', views.specific_industry_post_list_view, name="industry_post_list"),
    path('view_user_posts/', views.user_post_list_view, name="user_post_list"),
    path("verify-email/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
]
