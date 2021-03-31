from django.shortcuts import HttpResponse
from django.utils.decorators import decorator_from_middleware
from users.middlewares.activation import ValidateTokenMiddleware


@decorator_from_middleware(ValidateTokenMiddleware)
def activate_view(request, token):
    print('--- token', token)
    return HttpResponse('token = %s' % token)


@decorator_from_middleware(ValidateTokenMiddleware)
def reset_token(request, token):
    return HttpResponse('reset_token')
