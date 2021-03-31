from django.urls import path
# from .views import StoreList
from .views import store_list, store_details

app_name = 'stores'

urlpatterns = [
    path('', store_list, name='list'),
    path('<int:store_id>/', store_details, name='details'),
]
