import django_filters as df
from django.db.models import Q

from base.models import Person
from base.widgets import FormControlTextInput


class PersonFilter(df.FilterSet):
    text = df.CharFilter(
        method='filter_text',
        label='Recherche',
        widget=FormControlTextInput(attrs={'placeholder': 'Rechercher', 'name': 'id_name'}),
    )

    def filter_text(self, queryset, name, value):
        """
        Custom method to find if the searched value is in the first name, last name or surname of a person
        """
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(username__icontains=value)).distinct()

    class Meta:
        model = Person
        fields = ['text']
