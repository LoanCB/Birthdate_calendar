import datetime
import os

import requests
from django.core.management import BaseCommand

from base.models import Person


class Command(BaseCommand):
    help = 'Send a notification with ntfy'

    def handle(self, *args, **options):
        today = datetime.date.today().strftime('%d-%m')
        total = 0
        for person in Person.objects.all():
            if person.birthdate.strftime('%d-%m') == today:
                requests.post(
                    f"https://ntfy.sh/{os.getenv('TOPIC_NAME')}",
                    data=f"Aujourd'hui est l'anniversaire de {person.get_full_name()} !",
                    headers={
                        "Title": f"Anniversaire {person.get_full_name()}",
                        "Tags": "tada"
                    }
                )
                total += 1
        self.stdout.write(self.style.SUCCESS(f'Recherche terminée, {total} anniversaire(s) trouvé(s)'))

