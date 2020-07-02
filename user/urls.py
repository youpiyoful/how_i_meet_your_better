from django.urls import path

from . import views

urlpatterns = [
    path('account', views.my_account, name='my_account'),
]
