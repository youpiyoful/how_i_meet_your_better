from django.urls import path, include

from user import views

app_name = "user"
urlpatterns = [
    path("account/", views.my_account, name="my_account"),
    path("login", views.authentication, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("legal-mention", views.legal_mention, name="legal_mention"),
    path("record_favorite", views.record_favorite_substitute, name="record_favorite"),
    path("favorite", views.display_favorite_food, name="favorite_food"),
    # path("reset-password", include('django.contrib.auth.urls')),
    path("change-your-password", views.change_password, name="change_password")
]
