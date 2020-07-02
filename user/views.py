from django.shortcuts import render


# Create your views here.
def my_account(request):
    """render the account of user"""
    return render(request, 'user/account.html')
