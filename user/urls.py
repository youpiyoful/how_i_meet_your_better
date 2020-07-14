from django.urls import path

from . import views

urlpatterns = [
    path("account", views.my_account, name="my_account"),
    path("login", views.render_login_page, name="render_login_page"),
    path("loger", views.loger, name="loger"),
    path("logout", views.logout, name="logout"),
    path(
            "register",
            views.render_register_page,
            name="render_register_page"
        ),
    path("registration", views.registration, name="registration"),
]
