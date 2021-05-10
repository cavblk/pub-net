from django import forms
from django.db import models
from pubs.models import Product, Bundle


# order_by_choices = (
#     ('POPULARITY', 'Popularity'),
#     ('PRICE_ASC', 'Price ascending'),
#     ('PRICE_DESC', 'Price descending')
# )
class OrderBy(models.TextChoices):
    POPULARITY = 'popularity', 'Popularity'
    PRICE_ASC = 'price_asc', 'Price ascending'
    PRICE_DESC = 'price_desc', 'Price descending'


class SearchAndFilterBundle(forms.Form):
    search_term = forms.CharField(max_length=255, required=False, label='Search by name')
    order_by = forms.ChoiceField(choices=OrderBy.choices, required=False, label='Order by')
    products = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=(),
        required=False,
        label='products'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        products = Product.objects.all()
        product_choices = tuple([(product.id, product.name) for product in products])
        self.fields['products'].choices = product_choices

    def clean_products(self):
        products = self.cleaned_data.get('products', [])

        try:
            products = [int(product_id) for product_id in products]
        except ValueError:
            raise forms.ValidationError('Product IDs must be integers.')

        return products

    def get_filtered_bundle(self):
        # with is_valid Django creates the `cleaned_data` dictionary with all the cleaned informations.
        if self.is_valid():
            search_term = self.cleaned_data.get('search_term', None)
            order_by = self.cleaned_data.get('order_by', OrderBy.POPULARITY)
            products = self.cleaned_data.get('products', [])

            bundle_list = Bundle.objects.order_by('created_at')

            if search_term:
                bundle_list = bundle_list.filter(name__icontains=search_term)

            if order_by == OrderBy.PRICE_ASC:
                bundle_list = bundle_list.order_by('price')
            elif order_by == OrderBy.PRICE_DESC:
                bundle_list = bundle_list.order_by('-price')

            if products:
                # Version 1 - filter for at least one product.
                # bundle_list = bundle_list.filter(products__product__id__in=products)

                # Version 2 - filter by all products.
                # set_1 = {1, 2, 3}
                # set_2 = {1, 2, 3, 4, 5}
                # set_is is sub set of set_2 OR set_2 is super set of set_1
                products_set = set(products)
                bundle_ids = set()
                for bundle in bundle_list:
                    bundle_product_ids = set([
                        product_data[0]
                        for product_data in bundle.products.values_list('product__id')
                    ])

                    # if products_set.issubset(bundle_product_ids):
                    if bundle_product_ids.issuperset(products_set):
                        bundle_ids.add(bundle.id)

                bundle_list = bundle_list.filter(id__in=bundle_ids)

            return bundle_list

        return Bundle.objects.all()
