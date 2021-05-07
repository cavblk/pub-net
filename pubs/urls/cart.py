from django.urls import path
from pubs.views.cart import view

app_name = 'cart'

urlpatterns = [
    path('', view, name='view')
]
