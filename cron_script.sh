#! /bin/bash
source venv/bin/activate
#virtualenv is now active

./manage.py launch_data_fill
# ./manage.py coverage_script