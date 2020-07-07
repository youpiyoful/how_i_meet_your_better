from django.urls import path

from . import views

urlpatterns = [
    path('account', views.my_account, name='my_account'),
    path('login-page', views.render_login_page, name='render_login_page'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register-page', views.render_register_page, name='render_register_page'),
    path('regiter', views.register, name='register')
]
