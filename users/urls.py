from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import register_view

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('', include('django.contrib.auth.urls')),
    path('register/', register_view, name='register'),
]
