from django.shortcuts import (
    render,
    redirect,
    get_list_or_404,
    reverse,
    get_object_or_404,
)
from django.http import HttpResponse
from business.models import Product, Category, CategoriesProducts
from django.template import RequestContext
from business.food import Food
from business.form import SearchFoodForm


# Create your views here.
def index(request, message=False):
    """return the home template of our app"""
    form = SearchFoodForm()
    context = {'form': form}

    if message is not False:
        context['message'] = message

    return render(request, "business/index.html", context)



def results(request):
    """return the results of substitutions product"""

    product_name = request.GET.get('product_name')
    print("PRODUCT NAME : ", product_name)

    if product_name:
        food = Food(product_name)
        print('food ====== ', food)
        complete_product_and_its_categories = food.search_food_and_categories_by_product_name()

        if complete_product_and_its_categories == 'product not found':
            print('product not found')
            return redirect('index', message='Aucun produit ou catégorie associée trouvé')

        print("complete product and its categories : ", complete_product_and_its_categories)
        list_of_foods_substitute, commune_category = food.substitute_food_by_foods_with_best_nutriscore(
            complete_product_and_its_categories
        )
        print('list_of_foods_substitute : ', list_of_foods_substitute)

        if list_of_foods_substitute == 'this product have the best nutriscore':
            print('this product have the best nutriscore')
            return redirect('index', message="Ce produit ne possède aucun substitut de meilleur qualité")

        context = {
            "active_results": "active",
            "food_to_substitute": product_name,
            "origin_food_nutriscore": complete_product_and_its_categories.get('product').get('nutriscore'),
            "commune_category": commune_category,
            "url_image": complete_product_and_its_categories.get('product').get('image_url'),
            "foods_substitute": list_of_foods_substitute,
        }
        return render(request, "business/results.html", context)

    print("product_name is empty")
    return redirect("index", message="Le nom du produit ne doit pas être vide")


def detail_food(request):
    """display the page detail of food in params"""

    food = request.GET.get('food')
    product = Product.objects.get(product_name=food)
    categories = product.category_set.all().values('category_name')
    print("FOOD : ", food)
    print('PRODUCT : ', product)

    food_detail = {
        "name": product.product_name,
        "nutriscore": product.nutriscore,
        "level_gras": "high",
        "fat": round(product.fat, 2),
        "level_sugar": "low",
        "sugar": round(product.sugars, 2),
        "level_sel": "moderate",
        "salt": round(product.salt, 2),
        "level_satur_gras": "high",
        "saturated_fat": round(product.saturated_fat, 2),
        "link_open_food_fact": product.product_url,
        "category": categories,
        "url_image": product.image_url
    }

    context = {"food_detail": food_detail}
    return render(request, "business/food.html", context)
