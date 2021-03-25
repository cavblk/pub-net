from django.contrib import admin
from stores.models import Store, Pizza, Ingredient


# Register your models here.
admin.site.register(Store)
admin.site.register(Pizza)
admin.site.register(Ingredient)
