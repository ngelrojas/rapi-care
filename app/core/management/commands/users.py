from django.core.management.base import BaseCommand
from django.db import transaction
from core.user import User


class Command(BaseCommand):
    help = "provide user name and password"

    def success(self, message):
        return self.stdout.write(self.style.SUCCESS(message))

    def warning(self, message):
        return self.stdout.write(self.style.WARNING(message))

    def error(self, message):
        return self.stdout.write(self.style.ERROR(message))

    def handle(self, *args, **options):
        self.warning(
            "if something goes wrong after installations, \n"
            "please contact with the admin."
        )

        with transaction.atomic():
            try:
                User.objects.create_superuser("admin@flow.com", "admin2021")
                self.success("user admin created.")
            except Exception as err:
                self.error(f"{err}")
