import os

os.system("coverage run --source='user' --omit='user/__init__.py','user/admin.py','user/tests*','user/apps.py','user/urls.py','user/migrations/*'  manage.py test user")
os.system("coverage report")

os.system("coverage run --source='business' --omit='business/__init__.py','business/admin.py','business/tests*','business/apps.py','business/urls.py','business/migrations/*'  manage.py test business")
os.system("coverage report")