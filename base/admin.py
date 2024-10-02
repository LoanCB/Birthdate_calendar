from django.contrib import admin
from phonenumbers import PhoneNumberFormat, format_number

from base.models import Email, Person, CustomUser, PhoneNumber, Team

admin.site.register(CustomUser)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'birthdate',
        'get_teams',
        'get_emails',
        'get_phone_numbers'
    )
    search_fields = ('first_name', 'last_name', 'username')
    search_help_text = 'Vous pouvez rechercher sur le prénom, nom, le surnom'

    @admin.display(description='équipes')
    def get_teams(self, obj):
        return ', '.join([team.name for team in obj.teams.all()])

    @admin.display(description='emails')
    def get_emails(self, obj):
        return ', '.join([email.email for email in obj.emails.all()])

    @admin.display(description='Numéros de téléphone')
    def get_phone_numbers(self, obj):
        return ', '.join([format_number(phone_number.phone_number, PhoneNumberFormat.NATIONAL) for phone_number in obj.phone_numbers.all()])


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Email)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'get_person')

    @admin.display(description='Personne')
    def get_person(self, obj):
        return obj.person.get_full_name()


@admin.register(PhoneNumber)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('get_phone_number', 'title', 'get_person')

    @admin.display(description='Personne')
    def get_person(self, obj):
        return obj.person.get_full_name()

    @admin.display(description='Numéro de téléphone')
    def get_phone_number(self, obj):
        return format_number(obj.phone_number, PhoneNumberFormat.NATIONAL)
