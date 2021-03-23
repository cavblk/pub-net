from django.shortcuts import render, redirect, reverse
from users.forms import RegisterForm
from users.emails import send_register_email


# Create your views here.
def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:  # consider this is POST method only
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            send_register_email(user)
            return redirect(reverse('users:login'))

    return render(request, 'users/register.html', {
        'form': form
    })
