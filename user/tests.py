"""
Test for the user app
"""
from django.contrib.auth.models import User
from django.test import TestCase
# from django import forms
# from .forms import RegistrationForm
from .models import Favorite, PurBeurreUser
from business.models import Product


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

    def test_authentication(self):
        # send login data
        response = self.client.post('/my-account/login', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        assert (self.client.session['_auth_user_id'])

    def test_authentication_error(self):
        """
        test the behavior of login function when
        the error exist
        """
        response = self.client.post(
            '/my-account/login',
            {
                'username': 'test',
                'password': 'test',
                'connect': 'true'
            },
            follow=True
        )
        self.assertRaises(
            KeyError, lambda: self.client.session['_auth_user_id']
        )
        self.assertFalse(response.context['user'].is_authenticated)
        # TODO : vérifier le contenu

    def test_user_is_none(self):
        """
        test the behavior when user is none
        """
        response = self.client.post(
            '/my-account/login',
            {
                'username': 'inconnu',
                'password': 'secret'
            }
        )
        self.assertTrue(response.context['message'] == 'Utilisateur inconnu')


class RegisterTests(TestCase):
    """
    test the register view
    """
    def setUp(self):
        """
        init the setup of the test for register
        """
        # self.form = RegistrationForm()
        self.client.post('/my-account/register', {
            'firstname': 'yoan', 
            'lastname': 'Fornari', 
            'email': 'yoanfornari.same@gmail.com',
            'password_field': '123',
            'password_confirmation': '123'
        })

    def test_register_is_ok(self):
        """
        a post request for register account
        """
        response = self.client.post('/my-account/register', {
            'firstname': 'yoan', 
            'lastname': 'Fornari', 
            'email': 'yoanfornari@gmail.com',
            'password_field': '123',
            'password_confirmation': '123'},
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].is_valid)
        self.assertRedirects(response, '/my-account/login', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_register_when_form_is_not_valid(self):
        """
        Test the behavior when user send a form than is not valid
        """
        response = self.client.post('/my-account/register', {
            'firstname': 'yoan',
            'lastname': 'Fornari',
            'email': 'notOk',
            'password_field': '123',
            'password_confirmation': '123'
        })

        # self.assertFormError(response, 'form', 'email', ['Entrez une adresse mail valide'])
        self.assertContains(response, 'Entrez une adresse mail valide', status_code=200, html=True)
        # self.assertFieldOutput(self.form.form.email, {'a@a.com': 'a@a.com'}, {'aaa': ['Enter a valid email address.']})

    def test_account_already_exist(self):
        """
        test the behavior when account already register in db
        """
        response = self.client.post('/my-account/register', {
            'firstname': 'yoan', 
            'lastname': 'Fornari', 
            'email': 'yoanfornari.same@gmail.com',
            'password_field': '123',
            'password_confirmation': '123'
        })

        self.assertTrue(response.context['message'] == 'Votre compte existe déja')


class LogoutTests(TestCase):
    """
    test the logout view
    """

    def test_logout(self):
        """
        test when logout work
        """
        response = self.client.get('/my-account/logout', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

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

# endregion


# region TESTS OF MODELS
class FavoriteTests(TestCase):
    """
    test of favorite model
    """
    def test_the_str_return_of_favorite_model(self):
        """
        test than favorite model return substitut + product
        """
        substitute = Product(product_name="nocciolata")
        product = Product(product_name="nutella")
        favorite = Favorite(substitute=substitute, product=product)
        self.assertEqual(str(favorite), "Substitut : nocciolata / Produit : nutella")


class PurBeurreUserTest(TestCase):
    """
    test of purBeurreUser user extends model
    """
    def test_than_extend_of_user_default_model_return_username(self):
        """
        test than PureBeurreUser model return firstname + lastname as username
        """
        default_user = User(first_name="Yoan", last_name="Fornari")
        user = PurBeurreUser(user=default_user)
        self.assertEqual(str(user), "Compte de Yoan Fornari")
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