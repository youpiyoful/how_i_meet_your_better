from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """return the home template of our app"""
    return HttpResponse("Hello, world !")

