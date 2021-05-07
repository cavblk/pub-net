from django.shortcuts import render


def homepage_view(request):
    if request.user.is_authenticated:
        print('user_id', request.user.id)
        print('pubs', request.user.pubs)
        print('pubs', request.user.profile)

    return render(request, 'homepage.html', {
        'brand': 'Ye Olde New Pub',
        'motto': 'Probably the best Ye Olde New Pub in the area!',
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
