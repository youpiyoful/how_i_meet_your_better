import os

os.system("coverage run --source='.' --omit='venv/*','user/migrations/*'  manage.py test")
os.system("coverage report")