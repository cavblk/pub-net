from django.shortcuts import render


def homepage_view(request):
    if request.user.is_authenticated:
        print('user_id', request.user.id)
        print('stores', request.user.stores)
        print('stores', request.user.profile)

    return render(request, 'homepage.html', {
        'brand': 'Python Pizza',
        'motto': 'Probably the best pizza in the world!',
        'pizza_list': [{
            'name': 'Margherita',
            'price': 12
        }, {
            'name': 'Romana',
            'price': 14
        }]
    })


def contact_view(request):
    return render(request, 'contact.html')
