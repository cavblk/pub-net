from django.urls import path
from users.views.activation import activate_view, reset_token

app_name = 'activation'

urlpatterns = [
    path('activate/', activate_view, name='activate'),
    path('reset_token/', reset_token, name='reset_token'),
]
