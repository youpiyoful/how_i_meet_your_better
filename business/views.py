from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(request):
    """return the home template of our app"""
    # return HttpResponse("Hello world, look at this <a href='http://127.0.0.1:8000/himyb/Yoan%20Fornari/display_name'>link</a>")
    # template = loader.get_template('business/index.html')
    # context = {"coucou": "coucou"}
    return render(request, 'business/index.html')
    # return HttpResponse(template.render(request))

def display_name(request, name):
    """display the name past in params"""
    return HttpResponse("mon nom est %s" % name)

