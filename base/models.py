from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    user = models.ForeignKey(User, verbose_name='Utilisateur', related_name='persons', on_delete=models.CASCADE)
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
