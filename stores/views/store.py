from django.shortcuts import render, HttpResponse, Http404
from django.views.generic import ListView
from stores.models import Store


# Create your views here.
# class StoreList(ListView):
#     model = Store
#     template_name = 'stores/list.html'
#     context_object_name = 'store_list'

def store_list(request):
    search_by_name = request.GET.get('name')
    fee = request.GET.get('fee')

    if search_by_name:
        stores = Store.objects.filter(name__icontains=search_by_name).all()
    else:
        stores = Store.objects.all()

    if fee:
        stores = stores.filter(profit_fee=fee)

    return render(request, 'stores/list.html', {
        'store_list': stores
    })


def store_details(request, store_id):
    try:
        store = Store.objects.get(pk=store_id)
    except Store.DoesNotExist:
        raise Http404('Store with ID %s does not exist.' % store_id)

    return render(request, 'stores/details.html', {
        'store': store
    })
