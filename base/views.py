from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone

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

    # Get the current month and day
    current_month = timezone.now().month
    current_day = timezone.now().day

    next_persons_unfiltered = queryset.filter(birthdate__month__gte=current_month, birthdate__day__gte=current_day)
    if not next_persons_unfiltered:
        next_persons_unfiltered = queryset

    next_persons_unfiltered = [
        [person, int(f"{person.birthdate.month}{person.birthdate.day}")] for person in next_persons_unfiltered
    ]
    next_persons_filtered = sorted(next_persons_unfiltered, key=lambda x: x[1])
    try:
        next_persons = next_persons_filtered[0:3]
    except IndexError:
        try:
            next_persons = next_persons_filtered[0:2]
        except IndexError:
            next_persons = next_persons_filtered[0]

    try:
        persons = paginator.page(page)
    except PageNotAnInteger:
        persons = paginator.page(1)
    except EmptyPage:
        persons = paginator.page(paginator.num_pages)

    return render(request, 'base/home.html', {
        'persons': persons,
        'filter': f,
        'next_persons': [person[0] for person in next_persons]
    })
