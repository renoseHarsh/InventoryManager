from django.test import TestCase
from django.contrib.auth.models import User
from .models import *

class ModelTestCases(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username = 'testUser', password='testPassword')
        self.test_item = Item.objects.create(name= 'testItem', price = 10)
        self.test_location = Location.objects.create(name = 'testLocation', person = self.test_user.person)
        self.test_inventory = Inventory.objects.get(location=self.test_location, item=self.test_item)
        self.test_inventory.quantity = 5
        self.test_inventory.save()
        self.test_store = Store.objects.create(name='testStore', location = self.test_location)
        self.test_storeStatement = StoreStatement.objects.create(creator = self.test_user.person,
                                                            warehouse = self.test_location,
                                                            customer = self.test_store,
                                                            )
        self.test_itemQuantity = ItemQuantity.objects.create(statement = self.test_storeStatement,
                                                        item = self.test_item,
                                                        )


    def test_user_and_person_creation(self):
        person = self.test_user.person

        self.assertIsInstance(person, Person)
        self.assertEqual(person.user, self.test_user)
        self.assertEqual(person.full_name, None)
        self.assertEqual(person.number, None)
        self.assertFalse(person.is_owner)



    def test_inventory_creation_on_item_creation(self):
        new_test_item = Item.objects.create(name= 'testItem', price = 10)
        inventory = Inventory.objects.get(location = self.test_location, item=new_test_item)

        self.assertEqual(inventory.location, self.test_location)
        self.assertEqual(inventory.item, new_test_item)
        self.assertEqual(inventory.quantity, 0)


    def test_location_person_and_user_association(self):
        self.assertEqual(self.test_location.person ,self.test_user.person)


    def test_store_and_location_association(self):
        self.assertEqual(self.test_store.location, self.test_location)


    def test_store_statement_creation_attributes(self):
        self.assertEqual(self.test_storeStatement.creator, self.test_user.person)
        self.assertEqual(self.test_storeStatement.warehouse, self.test_location)
        self.assertEqual(self.test_storeStatement.customer, self.test_store)
        self.assertEqual(self.test_storeStatement.status, 'Pending')




    def test_item_quantity_attributes(self):
        self.assertEqual(self.test_itemQuantity.statement, self.test_storeStatement)
        self.assertEqual(self.test_itemQuantity.item, self.test_item)
        self.assertEqual(self.test_itemQuantity.quantity, 0)


    def test_StoreStatement_get_ST_Info(self):
        statement_info = self.test_storeStatement.get_ST_Info()

        self.assertEqual(statement_info['from'], self.test_location)
        self.assertEqual(statement_info['to'], self.test_store)
        self.assertEqual(statement_info['creator'], self.test_user.person)
        self.assertEqual(statement_info['status'], 'Pending')
        self.assertEqual(statement_info['itemList'][0], self.test_itemQuantity)
        self.assertEqual(statement_info['id'], self.test_storeStatement.id)

        price = sum(each.price for each in self.test_storeStatement.itemquantity_set.all())

        self.assertEqual(statement_info['price'], price)


    def test_Person_get_statement(self):
        data = self.test_user.person.get_statement()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'bg-info')


    def test_Person_has_location(self):
        self.assertTrue(self.test_user.person.has_location())
        self.test_location.person = None
        self.test_location.save()
        self.assertFalse(self.test_user.person.has_location())


    def test_Person_get_assigned_location_name(self):
        self.assertEqual(self.test_user.person.get_assigned_location_name(), self.test_location)
        self.test_user.person.location = None
        self.test_location.save()
        self.assertIsNone(self.test_user.person.get_assigned_location_name())


    def test_Person_inventory_for_assigned_location(self):
        self.assertEqual(self.test_user.person.inventory_for_assigned_location(),
                         self.test_location.get_inevn_data())

        self.test_user.person.location = None
        self.test_location.save()
        self.assertIsNone(self.test_user.person.inventory_for_assigned_location())

    def test_Location_creation(self):
        self.assertEqual(self.test_location.name, 'testLocation')
        self.assertEqual(self.test_location.person, self.test_user.person)

    def test_inventory_creation_on_location_creation(self):
        new_test_location = Location.objects.create(name = 'testNewLoc')
        inventory = Inventory.objects.get(location = new_test_location, item=self.test_item)

        self.assertEqual(inventory.location, new_test_location)
        self.assertEqual(inventory.item, self.test_item)
        self.assertEqual(inventory.quantity, 0)

    def test_Location_get_inevn_data(self):
        data = self.test_location.get_inevn_data()
        self.assertEqual(len(data['data']), 1)

        new_item = Item.objects.create(name='newItem', price=2)
        new_invent = Inventory.objects.get(item=new_item, location=self.test_location)
        new_invent.quantity = 3
        new_invent.save()
        data = self.test_location.get_inevn_data()

        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['name'], self.test_item.name)
        self.assertEqual(data['data'][0]['quan'], self.test_inventory.quantity)
        self.assertEqual(data['data'][0]['per'], self.test_item.price)
        self.assertEqual(data['data'][0]['totP'], self.test_inventory.price)

        self.assertEqual(data['total_price'], self.test_inventory.price + new_invent.price)

    def test_Location_get_statement(self):
        data = self.test_location.get_statement()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'bg-info')

    