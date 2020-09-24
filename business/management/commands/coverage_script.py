from django.core.management.base import BaseCommand, CommandError
import os

class Command(BaseCommand):
    help = "launch all the test with coverage print"

    def handle(self, *args, **otions):
        os.system("coverage run --source='user' --omit='user/__init__.py','user/admin.py','user/tests*','user/apps.py','user/urls.py','user/migrations/*'  manage.py test user.tests")
        os.system("coverage report")

        os.system("coverage run --source='business' --omit='business/__init__.py','business/admin.py','business/tests*','business/launch_data_fill.py','business/apps.py','business/urls.py','business/migrations/*'  manage.py test business.tests business.tests_unit")
        os.system("coverage report")