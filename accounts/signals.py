from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

@receiver(post_save, sender=User)
def create_person_profile(sender, instance, created, *args, **kwargs):
    if created:
        Person.objects.create(user=instance)


@receiver(post_save, sender=Location)
def create_inventory_for_location(sender, instance, created, *args, **kwargs):
    if created:
        items = Item.objects.all()
        for item in items:
            Inventory.objects.create(location=instance, item=item, quantity=0)

@receiver(post_save, sender=Item)
def create_inventory_for_item(sender, instance, created, *args, **kwargs):
    if created:
        locations = Location.objects.all()
        for location in locations:
            Inventory.objects.create(location=location, item=instance, quantity=0)

@receiver(post_save, sender=ItemQuantity)
def item_quantity_save(sender, instance, created, *args, **kwargs):
    content_type = instance.content_type.model
    object_id = instance.object_id
    item = instance.item
    quantity = instance.quantity
    
    if content_type=='storestatement':
        inventory = StoreStatement.objects.get(id=object_id).warehouse.get_inventory(item)
        inventory.pend -= quantity
        inventory.save()