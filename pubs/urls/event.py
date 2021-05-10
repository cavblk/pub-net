from django.urls import path
from pubs.views.bundle import list_view, add_to_cart


app_name = 'event'

urlpatterns = [
    path('', list_view, name='list'),
    # path('<int:bundle_id>/add_to_cart/', add_to_cart, name='add_to_cart'),
]
