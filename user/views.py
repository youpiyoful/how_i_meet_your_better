from django.shortcuts import render


# Create your views here.
def my_account(request):
    """render the account of user"""
    context = {
        "user": {
            "name": "Yoan Fornari",
            "email": "yoanfornari@gmail.com",
            "age": "28",
            "adresse": "45 cours du parc 21 000, Dijon",
        }
    }
    return render(request, "user/account.html", context)


def render_login_page(request):
    """return the render page for login"""
    context = {
        'login': 'Connexion',
        'url_image': '/static/user/assets/img/wheat-field-2554358_1920.jpg'
    }
    return render(request, "user/login.html", context)


def loger(request):
    """call login function with mail + password"""
    pass


def logout(request):
    """call the metodh logout and redirect on home page"""
    return render(request, "business/index.html")


def render_register_page(request):
    """return the register page"""
    context = {
        'register': 'Inscription',
        'url_image': '/static/user/assets/img/wheat-field-2554358_1920.jpg'
    }
    return render(request, "user/register.html", context)


def registration(request):
    """record a new user"""
    # render(request, 'coucou')
    pass
