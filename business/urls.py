from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('<name>/display_name', views.display_name, name='display_name'),
    path('results', views.results, name='results')
]