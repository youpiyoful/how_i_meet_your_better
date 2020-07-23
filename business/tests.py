"""
Test for the business app
"""
from django.test import TestCase
from models import Product, Category


# region TESTS OF VIEW
class IndexTests(TestCase):
    """
    test index view
    """
    pass


class ResultsTests(TestCase):
    """
    test the view results()
    """
    pass


class DetailFoodTests(TestCase):
    """
    test the view detail_food()
    """
    pass
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


# region TEST OF CLASSES
# endregion