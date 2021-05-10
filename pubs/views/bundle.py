from django.shortcuts import redirect, reverse, Http404, render
from django.views.generic import ListView
from django.core.paginator import Paginator
from pubs.models import Bundle
from pubs.forms.filter import SearchAndFilterBundle
from utils.cart import Cart


# class bundleList(ListView):
#     model = Bundle
#     context_object_name = 'bundle_list'
#     template_name = 'pubs/bundle/list.html'
#     paginate_by = 6
# SearchAndFilterBundle
def list_view(request):
    form = SearchAndFilterBundle(request.GET)
    bundle_list = form.get_filtered_bundle()
    paginator = Paginator(bundle_list, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'pubs/bundle/list.html', {
        'page_obj': page_obj,
        'form': form,
    })


def add_to_cart(request, bundle_id):
    page = request.POST.get('page', 1)
    next_url = request.GET.get('next')

    try:
        quantity = int(request.POST['quantity'])
    except ValueError as e:
        raise Http404(e)

    cart = Cart(request.user, request.session)
    cart.update(bundle_id, quantity)
        
    if next_url:
        return redirect(next_url)

    return redirect('%s?page=%s' % (
        reverse('pubs:bundle:list'),
        page
    ))
