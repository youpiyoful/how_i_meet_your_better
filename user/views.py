from django.shortcuts import render


# Create your views here.
def my_account(request):
    """render the account of user"""
    context = {
        'user':
            {
                'name': 'Yoan Fornari',
                'email': 'yoanfornari@gmail.com',
                'age': '28',
                'adresse': '45 cours du parc 21 000, Dijon'
            }
    }
    return render(request, 'user/account.html', context)
