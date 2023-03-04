from django.contrib import admin

from base.models import Person, CustomUser


admin.site.register(CustomUser)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthdate')
