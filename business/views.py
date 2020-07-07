from django.shortcuts import render
from django.http import HttpResponse

# from django.template import loader


# Create your views here.
def index(request):
    """return the home template of our app"""
    return render(request, "business/index.html")


def results(request):
    """return the results of substitutions product"""
    # TODO se servir du nom de l'aliment à substituer pour retrouver les
    # informations sur les autres aliments
    context = {
        "active_results": "active",
        "food_to_substitute": "nutella par exemple",
        "url_image": "https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.176.400.jpg",
        "foods_substitute": [
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
        ],
    }
    return render(request, "business/results.html", context)


def display_name(request, name):
    """display the name past in params"""
    return HttpResponse("mon nom est %s" % name)


def detail_food(request, food):
    """display the page detail of food in params"""
    # TODO se servir de food pour retrouver les infos concernant
    # l'aliment dans la base et les rendre à l'aide du contexte
    context = {'food_detail': {
            'name': 'nutella',
            'nutriscore': 'e',
            'link_open_food_fact': 'https://fr.openfoodfacts.org/produit/3017620421006/nutella-ferrero',
            'category': 'pâte à tartiner',
            'nutri_per_100g': 'de la merde',
            'url_image': '"https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.176.400.jpg'
        }
    }
    return render(request, 'business/food.html', context)
