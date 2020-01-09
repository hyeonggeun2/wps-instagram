from django.shortcuts import render, redirect

from members.forms import SignupForm


def index(request):
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }
    return render(request, 'index.html', context)

