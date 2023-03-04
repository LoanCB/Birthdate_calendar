import datetime

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
                try:
                    request = requests.post(
                        f"https://ntfy.sh/{person.user.notification_tag}",
                        data=f"Aujourd'hui est l'anniversaire de {person.get_full_name()} !",
                        headers={
                            "Title": f"Anniversaire {person.get_full_name()}",
                            "Tags": "tada"
                        }
                    )
                    request.raise_for_status()
                    total += 1
                except Exception as e:
                    self.stderr.write(f"Une erreur s'est produite lors de l'envoi de la notification : {e}")
        if total > 0:
            self.stdout.write(f'{total} anniversaire(s) trouvé(s)')

