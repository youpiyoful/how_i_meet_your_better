"""
Test for the business app
"""
from django.test import TestCase
from .models import Product, Category
from django.shortcuts import reverse, get_object_or_404


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
        self.response = self.client.get(
            reverse("business:results", kwargs={"product_name": "nutella"})
        )

    def test_than_results_return_the_correct_context(self):
        """
        test than context contain all the data request
        by the user and render the correct template
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertIn("nutriscore", self.response.context["foods_substitute"][0])
        self.assertIn("name", self.response.context["foods_substitute"][0])
        self.assertIn("category", self.response.context["foods_substitute"][0])
        self.assertIn("url_image", self.response.context["foods_substitute"][0])

    def test_the_list_of_food_substitute_contain_(self):
        """
        test than list of food substitute contain
        6 elements of food substitute
        """
        self.assertEqual(type(self.response.context["foods_substitute"]), list)
        self.assertEqual(len(self.response.context["foods_substitute"]), 6)

    def test_results_when_list_is_not_return(self):
        """
        when the list is not return the function
        provides an http404 exception
        """
        response = self.client.get("/himyb/results/empty")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Not Found", status_code=404)


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
