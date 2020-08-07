from django.shortcuts import render, redirect, get_list_or_404, reverse, get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.template import RequestContext

# from django.template import loader


# Create your views here.
def index(request, success=True):
    """return the home template of our app"""
    # if request.args.get('context'):
    #     context = {'success_is_ok': request.args.get('context')}
    #     return render(request, 'business/index.html', context)
    context = {}
    if success is not True:
        context = {'register_is_ok': 'Félicitation vous êtes désormais \
        inscrit sur notre site'}

    return render(request, "business/index.html", context)


# def page_not_found_view(request, exception=None):
#     """
#     display an unic page 404
#     """
#     return render(request, 'business/404.html')


def results(request, product_name):
    """return the results of substitutions product"""
    # TODO se servir du nom de l'aliment à substituer pour retrouver les
    # informations sur les autres aliments
    print('PRODUCT NAME : ', product_name)

    # TODO : think to delete the condition it's because data don't exist yet
    if product_name == 'empty':
        list_of_foods_substitute = get_list_or_404(Product, product_name=product_name)
        # print('list_of_foods_substitute : ', list_of_foods_substitute)

    if product_name:
        list_of_foods_substitute = [
            {
                "nutriscore": "A",
                "name": "nutella",
                "category": "pâte à tartiner",
                "url_image": "https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.176.400.jpg",
            },
            {
                "nutriscore": "B",
                "name": "coca",
                "category": "soda",
                "url_image": "business/assets/img/portfolio/thumbnails/2.jpg",
            },
            {
                "nutriscore": "B",
                "name": "coca",
                "category": "soda",
                "url_image": "business/assets/img/portfolio/thumbnails/2.jpg",
            },
            {
                "nutriscore": "B",
                "name": "coca",
                "category": "soda",
                "url_image": "business/assets/img/portfolio/thumbnails/2.jpg",
            },
            {
                "nutriscore": "B",
                "name": "coca",
                "category": "soda",
                "url_image": "business/assets/img/portfolio/thumbnails/2.jpg",
            },
            {
                "nutriscore": "B",
                "name": "coca",
                "category": "soda",
                "url_image": "business/assets/img/portfolio/thumbnails/2.jpg",
            },
        ]
        context = {
            "active_results": "active",
            "food_to_substitute": product_name,
            "url_image": "https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.176.400.jpg",
            "foods_substitute": list_of_foods_substitute
        }
        return render(request, "business/results.html", context)

    print('product_name is empty')
    return redirect('index')


def detail_food(request, food):
    """display the page detail of food in params"""
    # TODO se servir de food pour retrouver les infos concernant
    # l'aliment dans la base et les rendre à l'aide du contexte
    print('FOOD : ', food)
    # food_detail = get_object_or_404(Product, product_name=food)
    food_detail = {
            'name': 'nutella',
            'nutriscore': 'e',
            "level_gras": "high",
            "level_sugar": "low",
            "level_sel": "moderate",
            "level_satur_gras": "high",
            'link_open_food_fact': 'https://fr.openfoodfacts.org/produit/3017620421006/nutella-ferrero',
            'category': 'pâte à tartiner',
            'nutri_per_100g': 'de la merde',
            'url_image': '"https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.176.400.jpg'
    }

    context = {
        'food_detail': food_detail
    }
    return render(request, 'business/food.html', context)
