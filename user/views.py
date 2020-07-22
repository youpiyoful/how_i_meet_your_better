from django.shortcuts import render, redirect, reverse
from .forms import RegistrationForm, BaseForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.views.decorators.csrf import csrf_protect, csrf_exempt


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


# @csrf_protect
def authentication(request):
    """return the render page for login"""

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password_field')
        print(password)
        # create a form instance and populate it with data from the request:²
        # form = BaseForm(request.POST)
        print(email, password)
        user = authenticate(username=email, password=password)
        print('USER : ', user)
        if user is not None:
            print('USER CONNECTED')
            login(request, user)
            return redirect('index')

    form = BaseForm()
    context = {
        'login': 'Connexion',
        'url_image': 'user/assets/img/wheat-field-2554358_1920.jpg',
        'form': form
    }
    print(form)
    return render(request, "user/login.html", context)


def logout_view(request):
    """call the metodh logout and redirect on home page"""
    logout(request)
    return render(request, "business/index.html")


def register(request):
    """return the register page"""
    form = RegistrationForm()
    context = {
        'register': 'Inscription',
        'url_image': 'user/assets/img/wheat-field-2554358_1920.jpg',
        'form': form
    }

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password_field')
        password_confirmation = request.POST.get('password_confirmation')
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            print("form is valid")

            user = User.objects.filter(email=email)
            
            if not user.exists():
                # If a user is not registered, create a new one
                user = User.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password
                )
                return redirect('user:login')

            else:
                context.update({'message': 'votre compte existe déja'})
                # TODO add the message to the register form
                return render(request, "user/register.html", context)

    return render(request, "user/register.html", context)


def legal_mention(request):
    """render the html of legal mention"""
    return render(request, "user/legal_mention.html")

# def registration(request):
#     """record a new user"""
#     # context = {'register_is_ok': 'Félicitation vous êtes désormais inscrit sur notre site'}
#     # context = 'Félicitation vous êtes désormais inscrit sur notre site'
#     # return render(request, "business/index.html", context)
#     success = 'success'
#     return redirect('index', success=success)
