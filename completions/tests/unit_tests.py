""" This file is for unitest of the app completions"""
from django.test import TestCase
from business.models import Product
from completions import helpers
from django.test import tag
from django.db.models.functions import Length

import random


class MockResponseToGetAttr:
    """
    mock the response to the method
    getattr()
    """

    def __init__(self, my_object, attribute, default_value=None):
        """init the attribute of the mock"""
        self.my_object = my_object
        self.attribute = attribute
        self.default_value = default_value


    def get_attr(self):
        pass

# @tag('test_helpers')
class TestHelpers(TestCase):
    """
    test all the method of helpers file
    """
    def setUp(self):
        """
        create many products
        """
        i = 0

        while i < 30 :
            nutriscore = random.choice(['C', 'D'])

            if i % 2 == 0:
                nutriscore = random.choice(['A', 'B'])
            Product.objects.create(
                product_name=f"ac{i}",
                nutriscore=nutriscore,
                image_url=f'http://image/{i}',
                product_url=f'https://url/{i}',
                fat=1,
                saturated_fat=1,
                sugars=1,
                salt=1
            )
            i += 1
        test = Product.objects.all().order_by('-nutriscore')[:5]
        # test_2 = test[len(test)-5:]
        print(len(test))
        print(test[0].nutriscore)
        print(test[4].nutriscore)
        

    def test_get_completions_have_limit_of_15(self):
        """
        test than function return no more than 15
        elements
        """
        response = helpers.get_completions('ac')
        self.assertLess(len(response), 16)

    def test_get_completions_is_ordered_by_nutriscore(self):
        """
        test than completion is ordered by nutriscore from worse
        to better
        """
        response = helpers.get_completions('ac')
        test = ['b', 'a']
        self.assertFalse(test[1] > test[0])
        self.assertFalse('a' > 'b')
        print("response => ", response[1])
        print("===> ", Product.objects.get(product_name=response[1]))
        nutri_1 = Product.objects.get(product_name=response[1]).nutriscore
        nutri_0 = Product.objects.get(product_name=response[0]).nutriscore
        print(nutri_1, ' <= ', nutri_0)
        self.assertFalse(nutri_1 > nutri_0)
        self.assertTrue(nutri_1 <= nutri_0)
