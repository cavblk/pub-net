from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views.account import register_view

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('', include('django.contrib.auth.urls')),
    path('register/', register_view, name='register'),
    path('social-auth/', include('social_django.urls'))
]
