"""
Test for the user app
"""
from django.contrib.auth.models import User
from django.test import TestCase


# region TESTS OF VIEW
class LogInTests(TestCase):

    def setUp(self):
        self.credentials = {
            'email': 'yoanfornari@gmail.com',
            'password_field': '123'}

        self.register = {
            'first_name': 'yoan',
            'last_name': 'Fornari',
            'username': 'yoanfornari@gmail.com',
            'email': 'yoanfornari@gmail.com',
            'password': '123',
        }
        User.objects.create_user(**self.register)

    def test_login(self):
        # send login data
        response = self.client.post('/my-account/login', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)


# class RegisterTests(TestCase):
#     """
#     test the register view
#     """
#     pass


# class LogoutTests(TestCase):
#     """
#     test the logout view
#     """
#     pass

# class SimpleTest(TestCase):
#     def setUp(self):
#         """
#         test needs a client
#         """
#         self.client = Client()
#         User.objects.create_user(
#             username='yoan@gmail.com',
#             first_name='yoan',
#             last_name='Fornari',
#             email='yoan@gmail.com',
#             password='123'
#         )
#         pass

#     def test_mon_q(self):
#         """
#         test mon uc
#         """
#         user = User.objects.get(email='yoan@gmail.com')
#         self.assertEqual(user.first_name, 'yoan')

#     # def test_login_is_ok(self):
#     #     """
#     #     a post request for login
#     #     """
#     #     response = self.client.post('/my-account/login', {'username': 'yoan@gmail.com', 'password': '123'})

#     #     # check that the response is 200 OK.
#     #     self.assertEqual(response.status_code, 200)
#     #     # self.assertEqual(response.get('username'), 'yoan@gmail.com')


#     def test_register_is_ok(self):
#         """
#         a post request for register account
#         """
#         response = self.client.post('/my-account/register', {
#             'firstname': 'yoan', 
#             'lastname': 'Fornari', 
#             'email': 'yoanfornari@gmail.com',
#             'password_field': '123',
#             'password_confirmation': '123'},
#             follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertRedirects(response, '/my-account/login', status_code=302, target_status_code=200, fetch_redirect_response=True)
# endregion


# region TESTS OF MODELS
# class FavoriteTests(TestCase):
#     """
#     test of favorite model
#     """
#     pass


# class PurBeurreUser(TestCase):
#     """
#     test of purBeurreUser user extends model
#     """
#     pass
# endregion


# region TEST OF CLASS
# class OpenFoodFactsTests(TestCase):
#     """
#     test all the method of openFoodFact object
#     """
#     pass

#     def test_retrieve_category_is_ok():
#         """
#         this test is for the recuperation of data from open food fact api
#         """
#         pass

#     def insert_data_in_the_db_test(self):
#         """
#         this test verify when the insertion of data from openfoodfact in
#         our bd is excuted correctly
#         """
#         pass

#     def test_retrieve_category_encounter_a_problem(self):
#         """
#         test the behavior of retrieve_category function when
#         the api don't return the attempted data
#         """
#         pass
    
# endregion