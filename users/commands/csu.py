from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "Создание суперпользователя с email и паролем по умолчанию"

    def handle(self, *args, **options):
        email = "admin@admin.com"
        password = "admin"

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f"Пользователь с email {email} уже существует.")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f"Создаю суперпользователя с email {email}.")
        )

        user = User.objects.create(
            email=email, is_staff=True, is_superuser=True, is_active=True
        )

        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f"Суперпользователь с email {email} успешно создан.")
        )
