from django.urls import path

from . import views

urlpatterns = [
    path('account', views.my_account, name='my_account'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register')
]
