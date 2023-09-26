from django.contrib import admin

from base.models import Person, CustomUser, Team

admin.site.register(CustomUser)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthdate', 'get_teams')
    list_filter = ('first_name', 'last_name', 'username')

    @admin.display(description='équipes')
    def get_teams(self, obj):
        return ', '.join([team.name for team in obj.teams.all()])


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
