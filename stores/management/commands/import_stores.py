import os
import json
from django.core.management import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from stores.models import Store, Pizza, Ingredient, StoreIngredients, PizzaIngredients

AuthUserModel = get_user_model()


def get_pizza_list():
    with open(os.path.join('data', 'pizza.json')) as pizza_file:
        pizza = json.load(pizza_file)
    return pizza


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--file', '-f', type=str)

    def handle(self, *args, **options):
        file_path = options.get('file')

        if not file_path:
            raise CommandError('File not provided!')

        if not file_path.endswith('.json'):
            raise CommandError('Import supports .json files only!')

        file_path = os.path.join('data', file_path)
        try:
            with open(file_path) as import_file:
                stores = json.load(import_file)
        except FileNotFoundError as e:
            raise CommandError('File at %s was not found!' % file_path)

        pizza_list = get_pizza_list()

        try:
            with transaction.atomic():
                for store in stores:
                    # Create owner in DB
                    owner_data = store['owner']
                    db_user = AuthUserModel.objects.create_user(
                        first_name=owner_data['first_name'],
                        last_name=owner_data['last_name'],
                        username=owner_data['email'],
                        email=owner_data['email'],
                        is_staff=1,
                        password='python12345678'
                    )

                    db_store = Store(
                        owner=db_user,
                        name=store['name'],
                        logo=store['logo'],
                        delivery_fee=store['delivery_fee'],
                        profit_fee=store['profit_fee'],
                    )
                    db_store.save()

                    for pizza in pizza_list:
                        db_pizza = Pizza(
                            store=db_store,
                            name=pizza['name'],
                            image=pizza['image'],
                        )
                        db_pizza.save()

                        for ingredient in pizza['ingredients']:
                            db_ingredient = Ingredient.objects.filter(name=ingredient['name']).first()

                            if not db_ingredient:
                                db_ingredient = Ingredient(
                                    name=ingredient['name'],
                                    image=ingredient['image'],
                                )
                                db_ingredient.save()

                            db_store_ingredient = StoreIngredients.objects.filter(
                                store=db_store,
                                ingredient=db_ingredient
                            ).first()

                            if db_store_ingredient:
                                db_store_ingredient.stock = ingredient['stock']
                                db_store_ingredient.price = ingredient['price']
                            else:
                                db_store_ingredient = StoreIngredients(
                                    store=db_store,
                                    ingredient=db_ingredient,
                                    stock=ingredient['stock'],
                                    price=ingredient['price'],
                                )
                            db_store_ingredient.save()

                            db_pizza_ingredient = PizzaIngredients.objects.filter(
                                store_ingredient=db_store_ingredient,
                                pizza=db_pizza
                            ).first()

                            if db_pizza_ingredient:
                                db_pizza_ingredient.quantity = ingredient['quantity']
                            else:
                                db_pizza_ingredient = PizzaIngredients(
                                    pizza=db_pizza,
                                    store_ingredient=db_store_ingredient,
                                    quantity=ingredient['quantity'],
                                )
                            db_pizza_ingredient.save()
        except Exception as e:
            raise CommandError('Something wrong happened: [%s] %s' % (type(e).__name__, e))
