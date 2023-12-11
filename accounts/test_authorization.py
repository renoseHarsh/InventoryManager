from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorizationTestCase(TestCase):
    def setUp(self):
        self.empusername = 'emp'
        self.emppassword = 'emppassword'
        self.ownusername = 'own'
        self.ownpassword = 'ownpassword'

        self.emp = User.objects.create_user(username=self.empusername,
                                             password=self.emppassword)
        self.own = User.objects.create_user(username=self.ownusername,
                                              password=self.ownpassword)
        self.own.person.is_owner = True
        self.own.person.save()

    def test_login_page_unauthenticated(self):
        response = self.client.get(reverse('register'))
        self.assertRedirects(response,
                             reverse('login')+f'?next={reverse("register")}')
        

    def test_home_page_unauthenticated(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response,
                             reverse('login') + f'?next={reverse("home")}')
    
    def loginemp(self):
        self.client.login(username = self.empusername,
                          password = self.emppassword)
    def loginown(self):
        self.client.login(username = self.ownusername,
                          password = self.ownpassword)

    
    def test_home_page_unauthenticated_user(self):
        pass

    # Register Page ('register)
    def test_register_page_unauthenticated(self):
        response = self.client.get(reverse('register'))
        self.assertRedirects(response,
                             reverse('login') + f'?next={reverse("register")}')
        
    def test_register_page_authenticated_employee(self):
        self.loginemp()
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('userInfo'))
    
        
    def test_register_page_authenticated_owner(self):
        self.loginown()
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    

        