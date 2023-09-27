from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from base.forms import LoginForm


def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect(home)

        # TODO error message

    return render(request, 'base/login.html', {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, "Vous avez bien été déconnecté")  # TODO show messages on base_site.html
    return redirect(login_user)


@login_required
def home(request):
    return render(request, 'base/home.html')
