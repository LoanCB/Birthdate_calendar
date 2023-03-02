from django.db import models


class Person(models.Model):
    first_name = models.CharField('Prénom', max_length=20)
    last_name = models.CharField('Nom', max_length=30)
    birthdate = models.DateField("Date d'anniveraire")

    class Meta:
        verbose_name = 'Personne'
        verbose_name_plural = 'Personnes'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
