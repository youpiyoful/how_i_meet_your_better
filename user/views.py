from django.shortcuts import render  # , redirect
# from django.urls import reverse
from .forms import RegistrationForm, BaseForm


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


def login(request):
    """return the render page for login"""

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            print("form is valid")

    else:
        form = BaseForm()
        
    context = {
        'login': 'Connexion',
        'url_image': '/static/user/assets/img/wheat-field-2554358_1920.jpg',
        'form': form
    }
    return render(request, "user/login.html", context)


# def loger(request):
#     """call login function with mail + password"""
#     pass


def logout(request):
    """call the metodh logout and redirect on home page"""
    return render(request, "business/index.html")


def register(request):
    """return the register page"""
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        print(firstname, lastname, email, password, password_confirmation)
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("form is valid")

        # user = User.objects.filter(email=email)
        # if not user.exists():
        #     # If a user is not registered, create a new one
        #     user = User.objects.creat(
        #         email=email,
        #         name=firstname + lastname,
        #         password=password
        #     )
        #     return redirect(request, 'user/thanks.html', context={'message': 'merci'})
    else:
        form = RegistrationForm()

    context = {
        'register': 'Inscription',
        'url_image': '/static/user/assets/img/wheat-field-2554358_1920.jpg',
        'form': form
    }
    return render(request, "user/register.html", context)


# def registration(request):
#     """record a new user"""
#     # context = {'register_is_ok': 'Félicitation vous êtes désormais inscrit sur notre site'}
#     # context = 'Félicitation vous êtes désormais inscrit sur notre site'
#     # return render(request, "business/index.html", context)
#     success = 'success'
#     return redirect('index', success=success)
