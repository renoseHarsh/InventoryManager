from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    number = models.CharField(max_length=15, null=True, blank=True)
    is_owner = models.BooleanField(default=False)

    def get_statement(self):
        raw_statements = StoreStatement.objects.filter(creator=self).order_by('-created_at')
        statements = []
        color_map = {
            "Approved": "bg-success",
            "Rejected": "bg-danger",
            "Pending": "bg-info",
        }
        for each in raw_statements:
            data = each.get_ST_Info()
            data["status"] = color_map[data["status"]]
            statements.append(data)
        return statements

    def has_location(self):
        try:
            self.location
            return True
        except:
            return False

    def get_assigned_location_name(self):
        if self.has_location():
            return self.location
        else:
            return None

    def inventory_for_assigned_location(self):
        if self.has_location():
            return self.location.get_inevn_data()
        else:
            return None

    def __str__(self):
        return str(self.user)


class Location(models.Model):
    name = models.CharField(max_length=50)
    person = models.OneToOneField(
        Person, on_delete=models.SET_NULL, null=True, blank=True
    )
    def get_inevn_data(self):
        ivent = Inventory.objects.filter(location=self)
        lst = []
        total = 0
        for each in ivent:
            data = {
                "name": each.item.name,
                "quan": each.quantity,
                "per": each.item.price,
                "totP": each.quantity * each.item.price,
            }
            lst.append(data)
            total += data["totP"]
            
        return {'total_price': total, 'data':lst}

    def __str__(self):
        return self.name
    
    def get_statement(self):
        raw_statements = StoreStatement.objects.filter(warehouse=self).order_by('-created_at')
        statements = []
        color_map = {
            "Approved": "bg-success",
            "Rejected": "bg-danger",
            "Pending": "bg-info",
        }
        for each in raw_statements:
            data = each.get_ST_Info()
            data["status"] = color_map[data["status"]]
            statements.append(data)
        return statements


class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.location} - {self.item} - {self.quantity}"


class Store(models.Model):
    name = models.CharField(max_length=50)
    owner = models.CharField(max_length=25, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StoreStatement(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Location, on_delete=models.CASCADE)
    customer = models.ForeignKey(Store, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Rejected", "Rejected"),
        ],
        default="Pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Statement #{self.warehouse} - {self.customer}"

    def get_ST_Info(self):
        dataSt = {
            "from": self.warehouse,
            "to": self.customer,
            "creator": self.creator,
            "status": self.status,
            "itemList": self.itemquantity_set.all(),
            "created_at": self.created_at,
            "id": self.id,
        }
        dataSt["price"] = self.price
        return dataSt
    
    @property
    def price(self):
        return sum(item_quantity.price for item_quantity in self.itemquantity_set.all())
    

class ItemQuantity(models.Model):
    statement = models.ForeignKey(StoreStatement, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.item} - Qty: {self.quantity}"

    @property
    def price(self):
        return self.item.price * self.quantity
