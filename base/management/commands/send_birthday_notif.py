import datetime
from typing import Iterable

import requests
from django.core.management import BaseCommand

from base.models import Person


def send_notification(message: str, title: str, notification_tags: Iterable[str]):
    successes = 0
    errors = []
    for notification_tag in notification_tags:
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
            successes += 1
        except Exception as e:
            errors.append(e)

    return {'successes': successes, 'errors': errors}


class Command(BaseCommand):
    help = 'Send a notification with ntfy'

    def handle(self, *args, **options):
        today = datetime.date.today().strftime('%d-%m')
        today_year = datetime.datetime.today().year
        total_notifications, total_birthday_found, total_birthday_tomorrow_found = 0, 0, 0

        for person in Person.objects.all():
            if person.birthdate.strftime('%d-%m') == today:
                notification_tags = set()
                notification_tags.add(person.user.notification_tag)
                for team in person.teams.all():
                    for user in team.users.all():
                        notification_tags.add(user.notification_tag)

                response = send_notification(
                    f"Aujourd'hui est l'anniversaire de {person.username or person.get_full_name()} !\n Cela lui fait "
                    f"{today_year - person.birthdate.year} ans",
                    f"Anniversaire {person.get_full_name()}",
                    notification_tags
                )

                successes, errors = response['successes'], response['errors']
                if successes:
                    total_notifications += successes
                else:
                    error_messages = [error for error in errors]
                    self.stderr.writelines([
                        f"Une erreur s'est produite lors de l'envoi de la notification :",
                        error_messages
                    ])
                total_birthday_found += 1
            elif (person.birthdate - datetime.timedelta(days=7)).strftime('%d-%m') == today:
                notification_tags = set()
                notification_tags.add(person.user.notification_tag)
                for team in person.teams.all():
                    for user in team.users.all():
                        notification_tags.add(user.notification_tag)

                response = send_notification(
                    f"L'anniversaire de {person.username or person.get_full_name()} arrive dans 7 jours",
                    "Anniversaire en approche !",
                    notification_tags
                )

                successes, errors = response['successes'], response['errors']
                if successes > 0:
                    total_birthday_tomorrow_found += successes
                else:
                    error_messages = [error for error in errors]
                    self.stderr.writelines([
                        f"Une erreur s'est produite lors de l'envoi de la notification :",
                        error_messages
                    ])
                total_birthday_found += 1

        self.stdout.writelines([
            f"{total_notifications} notifications envoyées :",
            f"{total_birthday_found} anniversaire(s) aujourd'hui",
            f"{total_birthday_tomorrow_found} anniversaire(s) en approche"
        ])
