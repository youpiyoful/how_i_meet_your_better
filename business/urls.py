from django.urls import path

from . import views

app_name = "business"
urlpatterns = [
    # path('', views.index, name='index'),
    path("results/", views.results, name="results"),
    path("detail-food/", views.detail_food, name="detail_food"),
]
