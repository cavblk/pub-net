from django.shortcuts import render, HttpResponse, Http404
from django.views.generic import ListView
from pubs.models import Pubs


# Create your views here.
# class StoreList(ListView):
#     model = Pubs
#     template_name = 'pubs/list.html'
#     context_object_name = 'pub_list'

def pub_list(request):
    search_by_name = request.GET.get('name')
    fee = request.GET.get('fee')

    if search_by_name:
        pubs = Pubs.objects.filter(name__icontains=search_by_name).all()
    else:
        pubs = Pubs.objects.all()

    if fee:
        pubs = pubs.filter(profit_fee=fee)

    return render(request, 'pubs/list.html', {
        'pub_list': pubs
    })


def pub_details(request, pub_id):
    try:
        pub = Pubs.objects.get(pk=pub_id)
    except Pubs.DoesNotExist:
        raise Http404('Pubs with ID %s does not exist.' % pub_id)

    return render(request, 'pubs/details.html', {
        'pub': pub
    })
