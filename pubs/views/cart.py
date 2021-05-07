from django.shortcuts import render
from pubs.models import Pizza


def view(request):
    cart = request.session.get('cart', {})
    pizza_list = Pizza.objects.filter(id__in=cart.keys())

    return render(request, 'pubs/cart/view.html', {
        'pizza_list': pizza_list
    })
