from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from .models import Store


# Create your views here.
# class StoreList(ListView):
#     model = Store
#     template_name = 'stores/list.html'
#     context_object_name = 'store_list'

def store_list(request):
    print('request', request.GET)
    search_by_name = request.GET.get('name')
    fee = request.GET.get('fee')
    print('search_by_name', search_by_name)

    if search_by_name:
        stores = Store.objects.filter(name__icontains=search_by_name).all()
    else:
        stores = Store.objects.all()

    if fee:
        stores = stores.filter(profit_fee=fee)

    print('stores', stores)
    
    return render(request, 'stores/list.html', {
        'store_list': stores
    })


def store_details(request, store_id):
    return HttpResponse('I received store_id = %s' % store_id)
