"""
Test for the user app
"""
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import reverse
# from django import forms
# from .forms import RegistrationForm
from user.models import Favorite, PurBeurreUser
from business.models import Product, Category
from django.test import tag


# region TESTS OF VIEW
class LogInTests(TestCase):

    def setUp(self):
        self.credentials = {
            'email': 'gabin@gmail.com',
            'password_field': '123'}

        self.register = {
            'first_name': 'gabin',
            'last_name': 'fornari',
            'username': 'gabin@gmail.com',
            'email': 'gabin@gmail.com',
            'password': '123',
        }
        User.objects.create_user(**self.register)

    def test_authentication(self):
        # send login data
        response = self.client.post('/my-account/login', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(
            response,
            '/Vous%20vous%20%C3%AAtes%20connect%C3%A9%20avec%20succ%C3%A8s%20!',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True)
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

    def test_render_template_login(self):
        """
        test than get request return the correct template
        login.html with the correct context
        """
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['login'], 'Connexion')
        self.assertEqual(response.context['url_image'], 'user/assets/img/wheat-field-2554358_1920.jpg')
        self.assertContains(response, 'DOCTYPE', status_code=200)


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

    def test_render_template_register(self):
        """
        test than get request return the template
        register.html with the correct context
        """
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['register'], 'Inscription')
        self.assertEqual(response.context['url_image'], 'user/assets/img/wheat-field-2554358_1920.jpg')
        self.assertContains(response, 'DOCTYPE', status_code=200)


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

@tag('record_favorite')
class FavoriteRecordTests(TestCase):
    """
    test the record_favorite_substitute function
    """
    def setUp(self):
        """
        create a fake user
        """
        self.user = User.objects.create_user(
            password="1234",
            username="gabin@gmail.com",
            first_name="gabin",
            last_name="fornari",
            email="gabin@gmail.com"
        )
        self.product = Product.objects.create(
            id=15,
            product_name="invention",
            image_url="https://nutella.jpg",
            product_url="https://nutella.com",
            fat=1.5,
            sugars=2.3366,
            saturated_fat=0.555,
            salt=10.234,
            nutriscore="z",
        )
        self.substitute = Product.objects.create(
            id=16,
            product_name="substitute",
            image_url="https://nutella_sub.jpg",
            product_url="https://nutella_sub.com",
            fat=1.5,
            sugars=2.3366,
            saturated_fat=0.555,
            salt=10.234,
            nutriscore="a",
        )

        commune_cat = Category.objects.create(
            id=5,
            category_name="commune_cat",
            url_category="https://fake_url.com"
        )

        commune_cat.products.add(self.product)
        commune_cat.products.add(self.substitute)    

    def test_record_favorite_substitute_is_correctly_record(self):
        """
        test than function retrieve correctly the data and record
        the substitute and his product in favorite table
        """
        c = Client()
        c.login(username='gabin@gmail.com', password='1234')
        response = c.post('/my-account/record_favorite', {
            'substitute_name': self.substitute.product_name,
            'product_name': self.product.product_name,
        }, follow=True)
        self.assertContains(response, "gabin", status_code=200)

    def test_record_favorite_substitute_when_user_is_not_authenticated(self):
        """
        test than function redirect in the same page (page results) when
        user want record a substitute but is not logged
        """
        response = self.client.post('/my-account/record_favorite', {
            'substitute_name': self.substitute.product_name,
            'product_name': self.product.product_name,
        }, follow=True)
        print("response content : ", response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invention', status_code=200)

    def test_record_favorite_substitute_redirection(self):
        """
        test than the status_code = 302 for the redirection
        """
        response = self.client.post('/my-account/record_favorite', {
            'substitute_name': self.substitute.product_name,
            'product_name': self.product.product_name,
        })
        self.assertEqual(response.status_code, 302)


@tag('favorite')
class FavoriteFoodDisplayTests(TestCase):
    """
    tests about display_favorite_food endpoint
    """

    def setUp(self):
        """
        init the data with fake favorite products
        """
        fake_user = User.objects.create_user(
            first_name='yoan',
            last_name='fornari',
            email='yoanfornari@gmail.com',
            password=123,
            username='yoanfornari@gmail.com'
        )
        self.c = Client()
        self.c.login(username='yoanfornari@gmail.com', password=123)

        self.favorite_product = Product.objects.create(
            id=16,
            product_name="substitute",
            image_url="https://sub.jpg",
            product_url="https://sub.com",
            fat=1.5,
            sugars=2.3366,
            saturated_fat=0.555,
            salt=10.234,
            nutriscore="a",
        )
        self.replaced_food = Product.objects.create(
            id=15,
            product_name="bad food",
            image_url="https://bad.jpg",
            product_url="https://bad.com",
            fat=1.5,
            sugars=2.3366,
            saturated_fat=0.555,
            salt=10.234,
            nutriscore="z",
        )
        substitute_and_substituted = Favorite.objects.create(
            id=1,
            product_id=15,
            substitute_id=16
        )
        pur_beur_user = PurBeurreUser.objects.create(user=fake_user)
        favorite_of_user = pur_beur_user.favorites.add(substitute_and_substituted)
        self.list_of_favorite = pur_beur_user.favorites.all().values()

        
    def test_than_favorite_food_exist_and_display_page(self):
        """
        test than endpoint render the correct elements 
        in context when favorite exist
        """
        response = self.c.get(reverse('user:favorite_food'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            type(response.context['list_of_substitute_and_substituted']),
            list
            )
        # print('list_of : ', self.list_of_favorite)
        # for el in self.list_of_favorite:
        #     print(el.get('id'))
        self.assertEqual(
            response.context['list_of_substitute_and_substituted'][0]['substitute_name'],
            'substitute'
        )
        self.assertEqual(
            response.context['list_of_substitute_and_substituted'][0]['substituted_name'],
            'bad food'
        )
        self.assertEqual(
            response.context['list_of_substitute_and_substituted'][0]['link_to_detail_of_substitute'],
            'https://sub.com'
        )

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
    test of purBeurreUser user extends model an
    """
    def test_than_extend_of_user_default_model_return_username(self):
        """
        test than PureBeurreUser model return
        firstname + lastname as username
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