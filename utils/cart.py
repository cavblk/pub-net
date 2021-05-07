import json
from pubs.models import Cart as CartModel


class Cart:
    def __init__(self, user, session):
        self._user = user
        self._session = session
        self._data = session.get('cart', {})

    def update(self, pizza_id, quantity):
        pizza_id_key = str(pizza_id)

        if quantity == 0:
            if pizza_id_key in self._data:
                del self._data[pizza_id_key]
        else:
            self._data[pizza_id_key] = quantity

        self._save()

    def _save(self):
        try:
            cart_model = CartModel.objects.get(user=self._user)
            cart_model.data = json.dumps(self._data)
        except CartModel.DoesNotExist:
            cart_model = CartModel(user=self._user, data=json.dumps(self._data))

        cart_model.save()
        self._session['cart'] = self._data

    @staticmethod
    def load(user, session):
        try:
            cart_model = CartModel.objects.get(user=user)
            cart_data = json.loads(cart_model.data)
        except CartModel.DoesNotExist:
            cart_data = {}

        session['cart'] = cart_data
