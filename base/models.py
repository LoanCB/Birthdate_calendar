from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.crypto import get_random_string


class CustomUser(AbstractUser):
    notification_tag = models.CharField(
        'Tag de notification',
        help_text="Chaine de caractère aléatoire à renseigner dans l'application pour recevoir les notifications",
        max_length=20,
        default=get_random_string(20)
    )

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username


class Person(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Utilisateur',
        related_name='persons',
        on_delete=models.CASCADE
    )
    first_name = models.CharField('Prénom', max_length=20)
    last_name = models.CharField('Nom', max_length=30)
    username = models.CharField('Surnom', max_length=20, blank=True)
    birthdate = models.DateField("Date d'anniveraire")

    class Meta:
        verbose_name = 'Personne'
        verbose_name_plural = 'Personnes'

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_teams(self):
        return ', '.join([team.name for team in self.teams.all()])


class Team(models.Model):
    name = models.CharField('Nom', max_length=50)
    users = models.ManyToManyField(CustomUser, verbose_name='utilisateurs', related_name='teams')
    persons = models.ManyToManyField(Person, verbose_name='personnes', related_name='teams')

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'

    def __str__(self):
        return self.name
