from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('', include('users.urls.account')),
    path('activation/<str:token>/', include('users.urls.activation')),
]
