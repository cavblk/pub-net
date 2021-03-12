from django.shortcuts import render
from django.views.generic import ListView
from .models import Store


# Create your views here.
class StoreList(ListView):
    model = Store
    template_name = 'stores/list.html'
    context_object_name = 'store_list'
