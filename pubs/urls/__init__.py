from django.urls import path, include
from pubs.views.pub import pub_list, pub_details

app_name = 'pubs'

urlpatterns = [
    path('', pub_list, name='list'),
    path('<int:pub_id>/', pub_details, name='details'),
    path('bundle/', include('pubs.urls.bundle')),
    path('cart/', include('pubs.urls.cart')),
    path('reservation/', include('pubs.urls.reservation')),
    path('event/', include('pubs.urls.event')),
    path('gallery/', include('pubs.urls.gallery')),
]
