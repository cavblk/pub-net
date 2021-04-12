from django.shortcuts import redirect, reverse
from django.views.generic import ListView
from stores.models import Pizza


class PizzaList(ListView):
    model = Pizza
    context_object_name = 'pizza_list'
    template_name = 'stores/pizza/list.html'
    paginate_by = 3


def add_to_cart(request, pizza_id):
    quantity = request.POST['quantity']
    page = request.POST.get('page', 1)
    print('pizza_id', pizza_id)
    print('quantity', quantity)
    print('page', page)

    # Add to cart.
    if 'cart' in request.session:
        request.session['cart'][pizza_id] = quantity
        request.session.modified = True
    else:
        request.session['cart'] = {
            pizza_id: quantity
        }
    print('request.session', request.session['cart'])

    return redirect('%s?page=%s' % (
        reverse('stores:pizza:list'),
        page
    ))
