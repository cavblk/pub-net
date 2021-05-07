from django.db import models
from django.contrib.auth import get_user_model
from pub_net.models import CustomModel

AuthUserModel = get_user_model()


# Create your models here.
class Ingredient(CustomModel):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='ingredients', default=None)


class Pubs(CustomModel):
    owner = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name='pubs')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='pubs')
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    profit_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ingredients = models.ManyToManyField(Ingredient, through='PubsIngredients', related_name='pubs')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class PubsIngredients(CustomModel):
    # TABLE COLUMNS WILL BE: id, pub_id, ingredient_id, stock, price, created_at, updated_at
    pub = models.ForeignKey(Pubs, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredients')
    stock = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Pizza(CustomModel):
    pub = models.ForeignKey(Pubs, on_delete=models.CASCADE, related_name='pizza')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pizza')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ingredients = models.ManyToManyField(PubsIngredients, through='PizzaIngredients', related_name='pizza')


class PizzaIngredients(CustomModel):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    pub_ingredient = models.ForeignKey(PubsIngredients, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=1)


class Cart(CustomModel):
    user = models.OneToOneField(AuthUserModel, on_delete=models.CASCADE)
    data = models.JSONField(null=True)
