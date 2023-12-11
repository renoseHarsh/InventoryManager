from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
class AuthorizationTestCase(TestCase):
    def setUp(self):
        self.empusername = 'emp'
        self.emppassword = 'emppassword'
        self.ownusername = 'own'
        self.ownpassword = 'ownpassword'
        self.testusername = 'testUser'
        self.testpassword = 'testUser'

        self.emp = User.objects.create_user(username=self.empusername,
                                             password=self.emppassword)
        self.own = User.objects.create_user(username=self.ownusername,
                                              password=self.ownpassword)
        self.test_user = User.objects.create_user(username=self.testusername,
                                                  password=self.testpassword)
        self.own.person.is_owner = True
        self.own.person.save()
        self.test_location = Location.objects.create(name = 'testLocation',
                                                     person = self.emp.person)
        self.test_location.person = self.emp.person
        self.test_location.save()
        self.test_store = Store.objects.create(name='testStore',
                                               location = self.test_location)
        self.test_storeStatement = StoreStatement.objects.create(creator = self.emp.person,
                                                            warehouse = self.test_location,
                                                            customer = self.test_store,
                                                            )

    def isStatus200(self, response):
        self.assertEqual(response.status_code, 200)
    
    def isStatus404(self, response):
        self.assertEqual(response.status_code, 404)

    def isStatus403(self, response):
        self.assertEqual(response.status_code, 403)

    def isRedirect_userInfo(self, response):
        self.assertRedirects(response, reverse('userInfo'))

    def isRedirect_locationInfo(self, response):
        self.assertRedirects(response, reverse('locationInfo'))

    def isRedirect_login_custom(self, response, custom, arg = None):
        self.assertRedirects(response,
                        reverse('login') + f'?next={reverse(custom, args = arg)}')


        

    
    def loginemp(self):
        self.client.login(username = self.empusername,
                          password = self.emppassword)
    def loginown(self):
        self.client.login(username = self.ownusername,
                          password = self.ownpassword)
    def logintest(self):
        self.client.login(username = self.testusername,
                          password = self.testpassword)

    # Register Page ('register')
    def get_register_response(self):
        return self.client.get(reverse('register'))
    
    def test_register_page_unauthenticated(self):
        self.isRedirect_login_custom(self.get_register_response(),
                                     "register")
        
    def test_register_page_authenticated_employee(self):
        self.loginemp()
        self.isRedirect_userInfo(self.get_register_response())
    
    def test_register_page_authenticated_owner(self):
        self.loginown()
        self.isStatus200(self.get_register_response())
    
    # Login Page ('login')
    def get_login_response(self):
        return self.client.get(reverse('login'))
    
    def test_login_page_unauthenticated(self):
        self.isStatus200(self.get_login_response())
    
    def test_login_page_authenticated_employee(self):
        self.loginemp()
        self.isRedirect_userInfo(self.get_login_response())
           
    def test_login_page_authenticated_owner(self):
        self.loginown()
        self.assertRedirects(self.get_login_response(), reverse('home'))

    # Logout Page ('logout')
    def test_logout_page(self):
        self.loginown()
        self.assertRedirects(self.client.get(reverse('logout')),
                             reverse('login'))

    # Home Page('home')
    def get_home_response(self):
            return self.client.get(reverse('home'))

    def test_home_page_unauthenticated(self):
        response = self.get_home_response()
        self.isRedirect_login_custom(response, "home")
    
    def test_home_page_authenticated_employee(self):
        self.loginemp()
        self.isRedirect_userInfo(self.get_home_response())
        
    def test_home_page_authenticated_owner(self):
        self.loginown()
        self.isStatus200(self.get_home_response())
        
    # UserInfoEmp ('userInfo')
    def get_userInfoEmp_response(self):
        return self.client.get(reverse('userInfo')) 
    
    def test_UserInfoEmp_unauthenticated(self):
        self.isRedirect_login_custom(self.get_userInfoEmp_response(), 'userInfo')
        
    def test_UserInfoEmp_authenticated(self):
        self.loginemp()
        self.isStatus200(self.get_userInfoEmp_response())


    # UserInfoOwn ('userInfo')
    def get_userInfoOwn_response(self):
        return self.client.get(reverse('userInfo', args=[self.emp.id]))

    def test_UserInfoOwn_unauthenticated(self):
        self.isRedirect_login_custom(self.get_userInfoOwn_response(),
                                     'userInfo',
                                     arg=[self.emp.id])

    def test_UserInfoOwn_authenticated_employee(self):
        self.loginemp()
        self.isRedirect_userInfo(self.get_userInfoOwn_response())
    
    def test_UserInfoOwn_authenticated_owner(self):
        self.loginown()
        self.isStatus200(self.get_userInfoOwn_response())

    def test_UserInfoOwn_authenticated_owner_inccorect_id(self):
        self.loginown()
        self.isStatus404(self.client.get(reverse('userInfo', args=[9])))

    

    # showSt('showST')

    def get_showSt_response(self, arg = None):
        return self.client.get(reverse('showST',
                                       args=[arg if arg else self.test_storeStatement.id]))
    
    
    def test_showSt_unauthenticated(self):
        self.isRedirect_login_custom(self.get_showSt_response(),
                                     'showST',
                                     arg=[self.test_storeStatement.id])
        

    def test_UserInfoOwn_authenticated_employee_not_creator(self):
        self.logintest()
        self.isStatus403(self.get_showSt_response())
    
    def test_UserInfoOwn_authenticated_employee_creator(self):
        self.loginemp()
        self.isStatus200(self.get_showSt_response())
    
    def test_UserInfoOwn_authenticated_owner(self):
        self.loginown()
        self.isStatus200(self.get_showSt_response())

    def test_UserInfoOwn_authenticated_wrong_stCode(self):
        self.loginown()
        self.isStatus404(self.get_showSt_response(arg=8))

    # locationInfo('locationInfo')
    def get_locationInfo_response(self, arg = None):
        return self.client.get(reverse('locationInfo',
                                       args=[arg if arg else self.test_location.id]))
    
    def test_locationInfo_unauthenticated(self):
        self.isRedirect_login_custom(self.get_locationInfo_response(),
                                     'locationInfo',
                                     arg=[self.test_location.id])
    
    def test_locationInfo_authenticated_employee_not_creator(self):
        self.logintest()
        self.isStatus403(self.get_locationInfo_response())

    def test_locationInfo_authenticated_employee_creator(self):
        self.loginemp()
        self.isStatus200(self.get_locationInfo_response())
    
    def test_locationInfo_authenticated_owner(self):
        self.loginown()
        self.isStatus200(self.get_locationInfo_response())

    def test_locationInfo_authenticated_wrong_stCode(self):
        self.loginown()
        self.isStatus404(self.get_locationInfo_response(arg=8))

    # all update

    def get_all_update_response(self, context):
        return self.client.get(reverse(context))
    
    def test_all_update_get(self):
        self.loginemp()
        self.isRedirect_userInfo(self.get_all_update_response('update_location'))

        self.isRedirect_userInfo(self.get_all_update_response('update_assigned'))

        self.isRedirect_userInfo(self.get_all_update_response('update_FullName'))

        self.isRedirect_userInfo(self.get_all_update_response('update_UserName'))

        self.isRedirect_userInfo(self.get_all_update_response('update_Number'))