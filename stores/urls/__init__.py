from django.urls import path, include
from stores.views.store import store_list, store_details

app_name = 'stores'

urlpatterns = [
    path('', store_list, name='list'),
    path('<int:store_id>/', store_details, name='details'),
    path('pizza/', include('stores.urls.pizza')),
    path('cart/', include('stores.urls.cart')),
]
