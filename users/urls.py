from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('', include('django.contrib.auth.urls')),
]
