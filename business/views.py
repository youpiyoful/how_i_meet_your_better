from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader


# Create your views here.
def index(request):
    """return the home template of our app"""
    # return HttpResponse("Hello world, look at this <a href='http://127.0.0.1:8000/himyb/Yoan%20Fornari/display_name'>link</a>")
    # template = loader.get_template('business/index.html')
    # context = {"coucou": "coucou"}
    return render(request, 'business/index.html')
    # return HttpResponse(template.render(request))


def results(request):
    """return the results of substitutions product"""
    context = {
        'active_results': 'active',
        'food_to_substitute': 'nutella par exemple',
        'url_image': 'https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.176.400.jpg',
        'foods_substitute': [
            {   
                'nutriscore': 'A',
                'name': 'nutella',
                'category': 'pâte à tartiner',
                'url_image': 'https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.176.400.jpg'
            },
            {   
                'nutriscore': 'B',
                'name': 'coca',
                'category': 'soda',
                'url_image': 'business/assets/img/portfolio/thumbnails/2.jpg'
            },
            {   
                'nutriscore': 'B',
                'name': 'coca',
                'category': 'soda',
                'url_image': 'business/assets/img/portfolio/thumbnails/2.jpg'
            },
            {   
                'nutriscore': 'B',
                'name': 'coca',
                'category': 'soda',
                'url_image': 'business/assets/img/portfolio/thumbnails/2.jpg'
            },
            {   
                'nutriscore': 'B',
                'name': 'coca',
                'category': 'soda',
                'url_image': 'business/assets/img/portfolio/thumbnails/2.jpg'
            },
            {   
                'nutriscore': 'B',
                'name': 'coca',
                'category': 'soda',
                'url_image': 'business/assets/img/portfolio/thumbnails/2.jpg'
            }
        ]
    }
    return render(request, 'business/results.html', context)


def display_name(request, name):
    """display the name past in params"""
    return HttpResponse("mon nom est %s" % name)
