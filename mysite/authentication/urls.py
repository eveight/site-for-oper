from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='authentication/login_v1.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/login.html'), name='logout'),
    path('register/', views.register, name='register'),
]