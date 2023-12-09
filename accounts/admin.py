from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Location)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(Store)
admin.site.register(StoreStatement)
admin.site.register(ItemQuantity)
