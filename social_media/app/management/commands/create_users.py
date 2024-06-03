from django.core.management.base import BaseCommand
from app.models import AppUser
import os

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **kwargs):
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not AppUser.objects.filter(email=email).exists():
            AppUser.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} already exists'))


        # Create test users for managing freinds requests

        for i in range(0, 24):
            email = f'test{i}@test.com'
            password = "1234"
            first_name = f'test {i} first'
            last_name = f'test {i} last'

            user = AppUser.objects.get_or_create(
                email = email,
                password=password,
                first_name = first_name,
                last_name = last_name
            )