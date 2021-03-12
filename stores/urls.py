from django.urls import path
from .views import StoreList

app_name = 'stores'

urlpatterns = [
    path('', StoreList.as_view(), name='list')
]
