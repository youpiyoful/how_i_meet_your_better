from django.shortcuts import render, redirect, reverse
from .forms import RegistrationForm, BaseForm
from django.utils.http import urlencode
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Favorite, PurBeurreUser
from business.models import Product, Category
# from django.views.decorators.csrf import csrf_protect, csrf_exempt


# Create your views here.
def my_account(request):
    """render the account of user"""
    if request.user.is_authenticated:
        context = {
            "user": {
                "name": request.user.first_name,
                "email": request.user.email,
                "age": "28",
                "adresse": "45 cours du parc 21 000, Dijon",
            }
        }
        return render(request, "user/account.html", context)
    else:
        return redirect('index', message='Veuillez vous connectez !')


# @csrf_protect
def authentication(request):
    """return the render page for login"""
    form = BaseForm()
    context = {
        'login': 'Connexion',
        'url_image': 'user/assets/img/wheat-field-2554358_1920.jpg',
        'form': form,
    }

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password_field')
        print(password)
        # create a form instance and populate it with data from the request:
        # form = BaseForm(request.POST)
        user = authenticate(username=email, password=password)
        print('USER : ', user)

        if user is not None:
            print('user connected')
            login(request, user)
            return redirect('index', message='Vous vous êtes connecté avec succès !')

        else:
            print('utilisateur inconnu')
            context['message'] = 'Utilisateur inconnu'

    print('CONTEXT : ', context)
    print('FORM : ', form)
    return render(request, "user/login.html", context)


def logout_view(request):
    """call the metod logout and redirect on home page"""
    logout(request)
    return redirect('index', message="Vous êtes bien déconnecté !")


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
        # password_confirmation = request.POST.get('password_confirmation')
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # print('*******************************', form.is_valid())
        if form.is_valid():
            print("form is valid")
            # TODO : voir pour remplacer par get_or_create

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
                context.update({'message': 'Votre compte existe déja'})
                # TODO add the message to the register form
                return render(request, "user/register.html", context)
        else:
            print("form is not valid")
            print(form)
            context.update({'form': form})
            # context.add({'errors': form.errors})
            print('ERROR :', form.errors)
            print('CONTEXT :', context['form'].errors)

    print(context)
    return render(request, "user/register.html", context)


def legal_mention(request):
    """render the html of legal mention"""
    return render(request, "user/legal_mention.html")


def record_favorite_substitute(request):
    """
    this view get a substitute and his product
    and record the choice in the favorite table
    """
    product_name = request.POST.get('product_name')
    product_id = request.POST.get('product_id')
    substitute_id = request.POST.get('substitute_id')
    print('product and substitute :', product_id, substitute_id)
    product = Product.objects.get(id=product_id)
    substitute = Product.objects.get(id=substitute_id)

    if request.user.is_authenticated:
        current_user = request.user
        user = User.objects.get(id=current_user.id)
        print('Instance of current_user : ', user)
        print('current_user : ', current_user)
        print('current_user ID : ', current_user.id)
        favorite, created = Favorite.objects.get_or_create(
            product=product,
            substitute=substitute
        )
        print("favorite object : ", favorite)
        print("favorite object got created : ", created)
        user_and_favorite_link = PurBeurreUser.objects.create(
            user=user).favorites.add(favorite)
        print('user and favorite link : ', user_and_favorite_link)
        return redirect('user:my_account')

    base_url = reverse('business:results')
    query_string = urlencode({'product_name': product_name})
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)
    # TODO : ajouter un message pour dire qu'il faut être connecté pour pouvoir sauvegarder un aliment.


# def registration(request):
#     """record a new user"""
#     # context = {'register_is_ok': 'Félicitation vous êtes désormais inscrit sur notre site'}
#     # context = 'Félicitation vous êtes désormais inscrit sur notre site'
#     # return render(request, "business/index.html", context)
#     success = 'success'
#     return redirect('index', success=success)
