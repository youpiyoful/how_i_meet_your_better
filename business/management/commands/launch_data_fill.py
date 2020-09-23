from django.core.management.base import BaseCommand, CommandError
from business.open_food_facts import OpenFoodFact
from business.models import Category, Product


class Command(BaseCommand):
    help = "use for populate the db himyb with open food fact data"

    def handle(self, *args, **options):
        off = OpenFoodFact()
        # retrieve category
        off.retrieve_all_category_name_from_open_food_facts_api()
        # retrieve category from our db
        list_of_cat = Category.objects.all()[:150]
        # call method retrieve product with each cat in list_of_cat
        for cat in list_of_cat:
            off.retrieve_food_with_url_category(cat)
            self.stdout.write(self.style.SUCCESS('Successfully retrieve "%s"' % cat))