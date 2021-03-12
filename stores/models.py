from django.db import models
from django.contrib.auth import get_user_model
from nt_pizza_django.models import CustomModel

AuthUserModel = get_user_model()


# Create your models here.
class Ingredient(CustomModel):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='ingredients', default=None)


class Store(CustomModel):
    owner = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='stores')
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    profit_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ingredients = models.ManyToManyField(Ingredient, through='StoreIngredients', related_name='stores')


class StoreIngredients(CustomModel):
    # TABLE COLUMNS WILL BE: id, store_id, ingredient_id, stock, price, created_at, updated_at
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    stock = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Pizza(CustomModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='pizza')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pizza')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ingredients = models.ManyToManyField(StoreIngredients, through='PizzaIngredients', related_name='pizza')


class PizzaIngredients(CustomModel):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    store_ingredient = models.ForeignKey(StoreIngredients, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=1)
