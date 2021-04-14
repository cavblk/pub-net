from django.urls import path
from stores.views.cart import view

app_name = 'cart'

urlpatterns = [
    path('', view, name='view')
]
