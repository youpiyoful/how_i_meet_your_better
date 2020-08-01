from business.open_food_facts import OpenFoodFact
from business.models import Category, Product

cat = 'data exist'
off = OpenFoodFact()
# retrieve category
# if cat is None:
#     off.retrieve_all_category_name_from_open_food_facts_api()
# retrieve category from our db
list_of_cat = Category.objects.all()[:5]
# call method retrieve product with each cat in list_of_cat
for cat in list_of_cat:
    off.retrieve_food_with_url_category(cat)

