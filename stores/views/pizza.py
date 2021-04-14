from django.shortcuts import redirect, reverse, Http404
from django.views.generic import ListView
from stores.models import Pizza
from utils.cart import Cart


class PizzaList(ListView):
    model = Pizza
    context_object_name = 'pizza_list'
    template_name = 'stores/pizza/list.html'
    paginate_by = 3


def add_to_cart(request, pizza_id):
    page = request.POST.get('page', 1)
    next_url = request.GET.get('next')

    try:
        quantity = int(request.POST['quantity'])
    except ValueError as e:
        raise Http404(e)

    cart = Cart(request.user, request.session)
    cart.update(pizza_id, quantity)
        
    if next_url:
        return redirect(next_url)

    return redirect('%s?page=%s' % (
        reverse('stores:pizza:list'),
        page
    ))
