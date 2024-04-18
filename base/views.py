from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect

from base.filters import PersonFilter
from base.forms import LoginForm
from base.models import Person


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
    messages.success(request, "Vous avez bien été déconnecté")
    return redirect(login_user)


@login_required
def home(request):
    queryset = Person.objects.filter(Q(user=request.user) | Q(teams__users=request.user)).distinct()
    f = PersonFilter(request.GET, queryset=queryset)
    page = request.GET.get('page', 1)
    paginator = Paginator(f.qs, 15)

    try:
        persons = paginator.page(page)
    except PageNotAnInteger:
        persons = paginator.page(1)
    except EmptyPage:
        persons = paginator.page(paginator.num_pages)

    return render(request, 'base/home.html', {'persons': persons, 'filter': f})
