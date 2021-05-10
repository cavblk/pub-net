import os
import json
from django.core.management import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from pubs.models import Pubs, Bundle, Product, PubsProducts, BundleProducts

AuthUserModel = get_user_model()


def get_bundle_list():
    with open(os.path.join('data', 'bundle.json')) as bundle_file:
        bundle = json.load(bundle_file)
    return bundle


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

        bundle_list = get_bundle_list()

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

                    db_pub = Pubs(
                        owner=db_user,
                        name=store['name'],
                        logo=store['logo'],
                        delivery_fee=store['delivery_fee'],
                        profit_fee=store['profit_fee'],
                    )
                    db_pub.save()

                    for bundle in bundle_list:
                        db_bundle = Bundle(
                            store=db_pub,
                            name=bundle['name'],
                            image=bundle['image'],
                        )
                        db_bundle.save()

                        for product in bundle['products']:
                            db_product = Product.objects.filter(name=product['name']).first()

                            if not db_product:
                                db_product = Product(
                                    name=product['name'],
                                    image=product['image'],
                                )
                                db_product.save()

                            db_pub_product = PubsProducts.objects.filter(
                                store=db_pub,
                                product=db_product
                            ).first()

                            if db_pub_product:
                                db_pub_product.stock = product['stock']
                                db_pub_product.price = product['price']
                            else:
                                db_pub_product = PubsProducts(
                                    store=db_pub,
                                    product=db_product,
                                    stock=product['stock'],
                                    price=product['price'],
                                )
                            db_pub_product.save()

                            db_bundle_product = BundleProducts.objects.filter(
                                store_product=db_pub_product,
                                bundle=db_bundle
                            ).first()

                            if db_bundle_product:
                                db_bundle_product.quantity = product['quantity']
                            else:
                                db_bundle_product = BundleProducts(
                                    bundle=db_bundle,
                                    store_product=db_pub_product,
                                    quantity=product['quantity'],
                                )
                            db_bundle_product.save()
        except Exception as e:
            raise CommandError('Something wrong happened: [%s] %s' % (type(e).__name__, e))
