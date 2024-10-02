from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import PhoneNumberFormat, format_number


class CustomUser(AbstractUser):
    notification_tag = models.CharField(
        'Tag de notification',
        help_text="Chaîne de caractère aléatoire à renseigner dans l'application pour recevoir les notifications",
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
    birthdate = models.DateField("Date d’anniversaire")

    class Meta:
        verbose_name = 'Personne'
        verbose_name_plural = 'Personnes'

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_teams(self):
        return ', '.join([team.name for team in self.teams.all()])

    def get_age(self):
        return timezone.now().year - self.birthdate.year
    
    def get_emails(self):
        return ', '.join([email.email for email in self.emails.all()])
    
    def get_phone_numbers(self):
        return ', '.join([format_number(phone_number.phone_number, PhoneNumberFormat.NATIONAL) for phone_number in self.phone_numbers.all()])


class Team(models.Model):
    name = models.CharField('Nom', max_length=50)
    users = models.ManyToManyField(CustomUser, verbose_name='utilisateurs', related_name='teams')
    persons = models.ManyToManyField(Person, verbose_name='personnes', related_name='teams')

    class Meta:
        verbose_name = 'Équipe'
        verbose_name_plural = 'Équipes'

    def __str__(self):
        return self.name


class Email(models.Model):
    email = models.EmailField("Email", unique=True)
    title = models.CharField("Intitulé", max_length=255, blank=True)
    person = models.ForeignKey(
        Person,
        verbose_name="Personne",
        related_name="emails",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    def __str__(self) -> str:
        return self.email


class PhoneNumber(models.Model):
    phone_number = PhoneNumberField("Numéro de téléphone", unique=True)
    title = models.CharField("Intitulé", max_length=255, blank=True)
    person = models.ForeignKey(
        Person,
        verbose_name="Personne",
        related_name="phone_numbers",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Numéro de téléphone'
        verbose_name_plural = 'Numéros de téléphone'

    def __str__(self) -> str:
        return format_number(self.phone_number, PhoneNumberFormat.NATIONAL)
