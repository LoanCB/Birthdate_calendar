from django.contrib import admin

from base.models import Person, CustomUser, Team

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
    search_fields = ('first_name', 'last_name', 'username', 'phone_number')
    search_help_text = 'Vous pouvez rechercher sur le prénom, nom, le surnom et le numéro de téléphone'

    @admin.display(description='équipes')
    def get_teams(self, obj):
        return ', '.join([team.name for team in obj.teams.all()])

    @admin.display(description='emails')
    def get_emails(self, obj):
        return ', '.join([email.email for email in obj.emails.all()])

    @admin.display(description='Numéros de téléphone')
    def get_phone_numbers(self, obj):
        return ', '.join([phone_number.phone_number for phone_number in obj.phone_numbers.all()])


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
