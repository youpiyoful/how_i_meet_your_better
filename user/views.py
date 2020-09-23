from django.shortcuts import render, redirect, reverse
from user.forms import RegistrationForm, BaseForm
from django.utils.http import urlencode
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from user.models import Favorite, PurBeurreUser
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
            },
            # 'url_image': 'user/assets/img/wheat-field-2554358_1920.jpg'
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
                user, created = PurBeurreUser.objects.get_or_create(user=user)
                print(created)
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
    substitute_name = request.POST.get('substitute_name')
    print('product and substitute :', product_name, substitute_name)
    product = Product.objects.get(product_name=product_name)
    substitute = Product.objects.get(product_name=substitute_name)
    # categories = product.category_set.all().values('category_name')
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
        user, created = PurBeurreUser.objects.get_or_create(
            user=user)
        favorite_link = user.favorites.add(favorite)
        print('user and favorite link : ', favorite_link)
        return redirect('user:my_account')

    base_url = reverse('business:results')
    query_string = urlencode({
        'product_name': product_name,
        'message': 'Vous devez être connecté pour enregistrer un produit dans vos favoris'})
    print('query_string : ', query_string)
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)


def display_favorite_food(request):
    """
    this function render the page with favorite food of user
    who display a list of link to detail about the favorite 
    food
    """

    if request.user.is_authenticated:
        print('request.user : ', request.user)
        user = PurBeurreUser.objects.get(user=request.user)

        if user:
            list_of_favorites = user.favorites.all().values()
            print('USER : ', user.id)
            print('List_of_favorites : ', list_of_favorites)
            list_of_substitute_and_substituted = []

            for favorite in list_of_favorites:
                print('favorite : ', favorite)
                substitute = Product.objects.get(id=favorite.get('substitute_id'))
                substituted = Product.objects.get(id=favorite.get('product_id'))
                substitute_and_substituted = {
                    'substitute_name': substitute.product_name,
                    'substituted_name': substituted.product_name,
                    'link_to_detail_of_substitute': substitute.product_url # TODO : inutile ! 
                }
                list_of_substitute_and_substituted.append(substitute_and_substituted)
                print('substitute : ', substitute, ' / ', 'substituted : ', substituted)
            print('list_of_substitute_and_substituted : ', list_of_substitute_and_substituted)
            context = {
                "list_of_substitute_and_substituted": list_of_substitute_and_substituted,
                "counter": Counter()
            }
        
        else:
            context = {"any_favorite": "Aucun favoris enregistré pour l'instant"}

        return render(request, 'user/favorite.html', context)
    
    return redirect('index', message='Veuillez vous connectez !')




class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return ''

    def decrement(self):
        self.count -= 1
        return ''

    def double(self):
        self.count *= 2
        return ''