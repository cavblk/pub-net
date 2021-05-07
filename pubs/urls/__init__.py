from django.urls import path, include
from pubs.views.pub import pub_list, pub_details

app_name = 'pubs'

urlpatterns = [
    path('', pub_list, name='list'),
    path('<int:pub_id>/', pub_details, name='details'),
    path('pizza/', include('pubs.urls.pizza')),
    path('cart/', include('pubs.urls.cart')),
]
