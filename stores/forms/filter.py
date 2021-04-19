from django import forms
from django.db import models
from stores.models import Ingredient, Pizza


# order_by_choices = (
#     ('POPULARITY', 'Popularity'),
#     ('PRICE_ASC', 'Price ascending'),
#     ('PRICE_DESC', 'Price descending')
# )
class OrderBy(models.TextChoices):
    POPULARITY = 'popularity', 'Popularity'
    PRICE_ASC = 'price_asc', 'Price ascending'
    PRICE_DESC = 'price_desc', 'Price descending'


class SearchAndFilterPizza(forms.Form):
    search_term = forms.CharField(max_length=255, required=False, label='Search by name')
    order_by = forms.ChoiceField(choices=OrderBy.choices, required=False, label='Order by')
    ingredients = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=(),
        required=False,
        label='Ingredients'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ingredients = Ingredient.objects.all()
        ingredient_choices = tuple([(ingredient.id, ingredient.name) for ingredient in ingredients])
        self.fields['ingredients'].choices = ingredient_choices

    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients', [])

        try:
            ingredients = [int(ingredient_id) for ingredient_id in ingredients]
        except ValueError:
            raise forms.ValidationError('Ingredient IDs must be integers.')

        return ingredients

    def get_filtered_pizza(self):
        # with is_valid Django creates the `cleaned_data` dictionary with all the cleaned informations.
        if self.is_valid():
            search_term = self.cleaned_data.get('search_term', None)
            order_by = self.cleaned_data.get('order_by', OrderBy.POPULARITY)
            ingredients = self.cleaned_data.get('ingredients', [])

            pizza_list = Pizza.objects.order_by('created_at')

            if search_term:
                pizza_list = pizza_list.filter(name__icontains=search_term)

            if order_by == OrderBy.PRICE_ASC:
                pizza_list = pizza_list.order_by('price')
            elif order_by == OrderBy.PRICE_DESC:
                pizza_list = pizza_list.order_by('-price')

            if ingredients:
                # Version 1 - filter for at least one ingredient.
                # pizza_list = pizza_list.filter(ingredients__ingredient__id__in=ingredients)

                # Version 2 - filter by all ingredients.
                # set_1 = {1, 2, 3}
                # set_2 = {1, 2, 3, 4, 5}
                # set_is is sub set of set_2 OR set_2 is super set of set_1
                ingredients_set = set(ingredients)
                pizza_ids = set()
                for pizza in pizza_list:
                    pizza_ingredient_ids = set([
                        ingredient_data[0]
                        for ingredient_data in pizza.ingredients.values_list('ingredient__id')
                    ])

                    # if ingredients_set.issubset(pizza_ingredient_ids):
                    if pizza_ingredient_ids.issuperset(ingredients_set):
                        pizza_ids.add(pizza.id)

                pizza_list = pizza_list.filter(id__in=pizza_ids)

            return pizza_list

        return Pizza.objects.all()
