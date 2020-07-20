from django.urls import path

from . import views

app_name = 'business'
urlpatterns = [
    # path('', views.index, name='index'),
    path('<name>/display_name', views.display_name, name='display_name'),
    path('results', views.results, name='results'),
    path('<food>/detail-food', views.detail_food, name='detail_food'),
]