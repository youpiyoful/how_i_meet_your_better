"""
Test for the business app
"""
from django.test import TestCase
from .models import Product, Category
from django.shortcuts import reverse, get_object_or_404
from decimal import *
import random
import string
from django.utils.http import urlencode


# region TESTS OF VIEW
class IndexTests(TestCase):
    """
    test index view
    """

    def test_index_render_the_well_template(self):
        """
        test than '/' url return the index.html template
        and the correct context
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        # find text contain for each block of code
        self.assertContains(
            response, "Du gras, oui, mais de la qualité !", status_code=200
        )
        self.assertContains(response, "Colette et Remy", status_code=200)
        self.assertContains(response, "Contactez-nous !", status_code=200)


class ResultsTests(TestCase):
    """
    test the view results()
    """

    def setUp(self):
        """
        init the response for get request
        """
        range_int = [i for i in range(11)]
        range_letter = [i for i in string.ascii_letters][:4]
        self.product = Product.objects.create(
            id=12,
            product_name="nutella",
            image_url="https://nutella.jpg",
            product_url="https://nutella.com",
            fat=1.5,
            sugars=2.3366,
            saturated_fat=0.555,
            salt=10.234,
            nutriscore="z",
        )

        self.best_product_ever = Product.objects.create(
            id=13,
            product_name="best product ever",
            image_url="https://best_product.jpg",
            product_url="https://best_product.com",
            fat=1.5,
            sugars=2.3366,
            saturated_fat=0.555,
            salt=10.234,
            nutriscore="a",
        )

        self.category = Category.objects.create(
            id=1,
            category_name="petit dej",
            url_category="https://petit_dej_au_lit.com"
        )
        self.category2 = Category.objects.create(
            id=2,
            category_name="petit dej2",
            url_category="https://petit_dej_au_lit.com2"
        )
        self.category3 = Category.objects.create(
            id=3,
            category_name="petit dej3",
            url_category="https://petit_dej_au_lit3.com"
        )
        self.category4 = Category.objects.create(
            id=4,
            category_name="petit dej4",
            url_category="https://petit_dej_au_lit4.com"
        )
        self.category5 = Category.objects.create(
            id=5,
            category_name="petit dej5",
            url_category="https://petit_dej_au_lit5.com"
        )
        self.category.products.add(self.product, through_defaults={
            'hyerarchie_score': 5
        })
        self.category2.products.add(self.product, through_defaults={
            'hyerarchie_score': 2
        })
        self.category3.products.add(self.product, through_defaults={
            'hyerarchie_score': 3
        })
        self.category4.products.add(self.product, through_defaults={
            'hyerarchie_score': 1
        })
        self.category5.products.add(self.product, through_defaults={
            'hyerarchie_score': 4
        })
        self.category.products.add(self.best_product_ever, through_defaults={
            'hyerarchie_score': 5
        })
        self.category2.products.add(self.best_product_ever, through_defaults={
            'hyerarchie_score': 2
        })
        self.category3.products.add(self.best_product_ever, through_defaults={
            'hyerarchie_score': 3
        })
        self.category4.products.add(self.best_product_ever, through_defaults={
            'hyerarchie_score': 1
        })
        self.category5.products.add(self.best_product_ever, through_defaults={
            'hyerarchie_score': 4
        })
        # self.food = food.Food("invention")
        i = 0

        while i < 10:
            product = Product.objects.create(
                id=i,
                product_name=f"invention{i}",
                image_url=f"https://nutella{i}.jpg",
                product_url=f"https://nutella{i}.com",
                fat=random.choice(range_int),
                sugars=random.choice(range_int),
                saturated_fat=random.choice(range_int),
                salt=random.choice(range_int),
                nutriscore=random.choice(range_letter),
            )
            if product.nutriscore > "c":
                self.category.products.add(product, through_defaults={
                    'hyerarchie_score': 5
                })
                self.category2.products.add(product, through_defaults={
                    'hyerarchie_score': 2
                })

            self.category3.products.add(product, through_defaults={
                'hyerarchie_score': 3
            })
            i += 1
        query_string = urlencode({"product_name": "nutella"})
        base_url = reverse("business:results")
        self.url = f'{base_url}?{query_string}'
        self.response = self.client.get(
            self.url
        )

    def test_than_results_return_the_correct_context(self):
        """
        test than context contain all the data request
        by the user and render the correct template
        """

        response = self.client.get(
            self.url,
            follow=True
        )
        print('context : ', response.context[0])
        self.assertEqual(response.status_code, 200)
        for elt in response.context:
            self.assertIn("origin_food_nutriscore", elt)
            self.assertIn("food_to_substitute", elt)
            self.assertIn("commune_category", elt)
            self.assertIn("url_image", elt)
            self.assertIn("foods_substitute", elt)

    def test_the_list_of_food_substitute_contain_(self):
        """
        test than list of food substitute contain
        6 elements of food substitute
        """
        print('self.context ======= ', self.response.context)
        self.assertEqual(type(self.response.context["foods_substitute"]), list)
        self.assertTrue(len(self.response.context["foods_substitute"]) <= 6)
        print("manon la pute : ", self.response.context["foods_substitute"])
        substitute = self.response.context["foods_substitute"][0]
        self.assertIn("nutriscore", substitute)
        self.assertIn("product_name", substitute)
        # self.assertIn("")

    # def test_results_when_list_is_not_return(self):
    #     """
    #     when the list is not return the function
    #     provides an http404 exception
    #     """
    #     response = self.client.get("/himyb/results/empty")
    #     self.assertEqual(response.status_code, 404)
    #     self.assertContains(response, "Not Found", status_code=404)

    # def test_when_product_name_is_empty(self):
    #     """
    #     test than function redirect to the home page
    #     when the product_name is an empty string
    #     """
    #     response = self.client.get(reverse(
    #         "business:results", kwargs={"product_name": ""}
    #     ), follow=True)
    #     self.assertContains(response, "rechercher", 200)


class DetailFoodTests(TestCase):
    """
    test the view detail_food()
    """

    # def setUp(self):
    #     """
    #     create a product
    #     """
    #     Product(product_name="nutella")

    def test_detail_food_is_ok(self):
        """
        test than detail_food return the page detail food
        with element about substitute choose by the user
        """
        response = self.client.get(
            reverse("business:detail_food", kwargs={"food": "nutella"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name", status_code=200)
        self.assertContains(response, "nutriscore", status_code=200)


# class PageNotFound(TestCase):
#     """
#     test the personalize view 404 page not found
#     """
#     def test_render_page_not_found_is_ok(self):
#         """
#         test than view page not found render the well template
#         """
#         response = get_object_or_404(Product, product_name='coucou')
#         self.assertContains(response, '404 error', status_code=404)

# endregion


# region TEST OF MODELS
class ProductModelTests(TestCase):
    """
    test the product model
    """

    def test_str_function_return_the_product_name(self):
        """
        test the return of the product model
        """
        product = Product(product_name="pizza")
        self.assertEqual(str(product), product.product_name)


class CategoryModelTests(TestCase):
    """
    test the category model
    """

    def test_category_return_the_category_name(self):
        """
        test the return of the category model
        """
        category = Category(category_name="petit déjeuner")
        self.assertEqual(str(category), category.category_name)


# endregion
