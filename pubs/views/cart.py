from django.shortcuts import render
from pubs.models import Bundle


def view(request):
    cart = request.session.get('cart', {})
    bundle_list = Bundle.objects.filter(id__in=cart.keys())

    return render(request, 'pubs/cart/view.html', {
        'bundle_list': bundle_list
    })
