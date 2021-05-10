from django.db import models
from django.contrib.auth import get_user_model
from pub_net.models import CustomModel

AuthUserModel = get_user_model()


# Create your models here.
class Product(CustomModel):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='products', default=None)


class Pubs(CustomModel):
    owner = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name='pubs')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='pubs')
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    profit_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    products = models.ManyToManyField(Product, through='PubsProducts', related_name='pubs')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class PubsProducts(CustomModel):
    # TABLE COLUMNS WILL BE: id, pub_id, product_id, stock, price, created_at, updated_at
    pub = models.ForeignKey(Pubs, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    stock = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Bundle(CustomModel):
    pub = models.ForeignKey(Pubs, on_delete=models.CASCADE, related_name='bundle')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='bundle')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    products = models.ManyToManyField(PubsProducts, through='BundleProducts', related_name='bundle')


class BundleProducts(CustomModel):
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    pub_product = models.ForeignKey(PubsProducts, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=1)


class Cart(CustomModel):
    user = models.OneToOneField(AuthUserModel, on_delete=models.CASCADE)
    data = models.JSONField(null=True)
