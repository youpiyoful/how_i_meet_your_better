from django.urls import path

from . import views

app_name = 'business'
urlpatterns = [
    # path('', views.index, name='index'),
    path('results/<product_name>', views.results, name='results'),
    path('<food>/detail-food', views.detail_food, name='detail_food'),
]
