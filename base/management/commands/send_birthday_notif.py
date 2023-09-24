import datetime

import requests
from django.core.management import BaseCommand

from base.models import Person


def send_notification(message: str, title: str, notification_tag: str):
    try:
        request = requests.post(
            f"https://ntfy.sh/{notification_tag}",
            data=message,
            headers={
                "Title": title,
                "Tags": "tada"
            }
        )
        request.raise_for_status()
        return {'success': True, 'error': None}
    except Exception as e:
        return {'success': False, 'error': e}


class Command(BaseCommand):
    help = 'Send a notification with ntfy'

    def handle(self, *args, **options):
        today = datetime.date.today().strftime('%d-%m')
        today_year = datetime.datetime.today().year
        total = 0
        total_tomorow = 0
        for person in Person.objects.all():
            if person.birthdate.strftime('%d-%m') == today:
                [success, error] = send_notification(
                    f"Aujourd'hui est l'anniversaire de {person.username or person.get_full_name()} !\n Cela lui fait "
                    f"{today_year - person.birthdate.year} ans",
                    f"Anniversaire {person.get_full_name()}",
                    person.user.notification_tag
                )
                if success:
                    total += 1
                else:
                    self.stderr.write(f"Une erreur s'est produite lors de l'envoi de la notification : {error}")
            elif (person.birthdate - datetime.timedelta(days=7)).strftime('%d-%m') == today:
                [success, error] = send_notification(
                    f"L'anniversaire de {person.username or person.get_full_name()} arrive dans 7 jours",
                    "Anniversaire en approche !",
                    person.user.notification_tag
                )
                if success:
                    total_tomorow += 1
                else:
                    self.stderr.write(f"Une erreur s'est produite lors de l'envoi de la notification : {error}")
        if total > 0:
            self.stdout.write(f'{total} anniversaire(s) trouvé(s)')
        if total_tomorow > 0:
            self.stdout.write(f"{total_tomorow} anniversaire(s) en approche")
