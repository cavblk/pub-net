from django import template

register = template.Library()


@register.filter(name='pagination_url')
def get_pagination_url(request, page_number=1):
    encoded_url = request.GET.urlencode() or ''
    old_page = request.GET.get('page')
    if old_page:
        encoded_url = encoded_url.replace('?', '').replace('page=%s' % old_page, '')
    print('encoded_url')

    if encoded_url:
        if encoded_url[-1] == '&':
            encoded_url = encoded_url[:-1]
        return '?%s&page=%s' % (encoded_url, page_number)

    return '?page=%s' % page_number
