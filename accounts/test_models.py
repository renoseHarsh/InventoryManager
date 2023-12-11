from django.test import TestCase
from django.contrib.auth.models import User
from .models import *

class ModelTestCases(TestCase):
    def setUp(self):
        pass


    def test_user_and_person_creation(self):
        test_user = User.objects.create(username = 'testUser', password='testPassword')
        person = test_user.person

        self.assertIsInstance(person, Person)
        self.assertEqual(person.user, test_user)
        self.assertEqual(person.full_name, None)
        self.assertEqual(person.number, None)
        self.assertFalse(person.is_owner)

    def test_inventory_creation_on_location_creation(self):
        test_item = Item.objects.create(name= 'testItem', price = 10)
        test_location = Location.objects.create(name = 'testLocation')
        inventory = Inventory.objects.get(location = test_location, item=test_item)

        self.assertEqual(inventory.location, test_location)
        self.assertEqual(inventory.item, test_item)
        self.assertEqual(inventory.quantity, 0)

    def test_inventory_creation_on_item_creation(self):
        test_location = Location.objects.create(name = 'testLocation')
        test_item = Item.objects.create(name= 'testItem', price = 10)
        inventory = Inventory.objects.get(location = test_location, item=test_item)

        self.assertEqual(inventory.location, test_location)
        self.assertEqual(inventory.item, test_item)
        self.assertEqual(inventory.quantity, 0)


    def test_statement_information_retrieval(self):
        test_user = User.objects.create(username='testUser', password='testPassword')
        test_location = Location.objects.create(name='testLocation', person=test_user.person)
        self.assertEqual(test_user.person, test_location.person)

        test_item = Item.objects.create(name='testItem', price=10)
        test_inventory = Inventory.objects.get(location=test_location, item=test_item)
        test_inventory.quantity = 5
        test_inventory.save()

        test_store = Store.objects.create(name='testStore', location = test_location)
        self.assertEqual(test_location, test_store.location)

        test_storeStatement = StoreStatement.objects.create(creator = test_user.person,
                                                            warehouse = test_location,
                                                            customer = test_store,
                                                            )
        
        self.assertEqual(test_storeStatement.creator, test_user.person)
        self.assertEqual(test_storeStatement.warehouse, test_location)
        self.assertEqual(test_storeStatement.customer, test_store)
        self.assertEqual(test_storeStatement.status, 'Pending')



        test_itemQuantity = ItemQuantity.objects.create(statement = test_storeStatement,
                                                        item = test_item,
                                                        )

        self.assertEqual(test_itemQuantity.statement, test_storeStatement)
        self.assertEqual(test_itemQuantity.item, test_item)
        self.assertEqual(test_itemQuantity.quantity, 0)

        statement_info = test_storeStatement.get_ST_Info()

        self.assertEqual(statement_info['from'], test_location)
        self.assertEqual(statement_info['to'], test_store)
        self.assertEqual(statement_info['creator'], test_user.person)
        self.assertEqual(statement_info['status'], 'Pending')
        self.assertEqual(statement_info['itemList'][0], test_itemQuantity)

        price = sum(each.price for each in test_storeStatement.itemquantity_set.all())

        self.assertEqual(statement_info['price'], price)





