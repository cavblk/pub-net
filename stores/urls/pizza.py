from django.urls import path
from stores.views.pizza import PizzaList, add_to_cart


app_name = 'pizza'

urlpatterns = [
    path('', PizzaList.as_view(), name='list'),
    path('<int:pizza_id>/add_to_cart/', add_to_cart, name='add_to_cart'),
]
