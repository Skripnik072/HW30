from django.core.management.base import BaseCommand

from users.models import Payment, User


class Command(BaseCommand):
    help = 'Добавление плательщика в БД'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(email='petrov@mail.ru')

        payments = [{'user': user, 'date': '2025-10-18', 'amount': 50000, 'payment_method': 'перевод'},
                   {'user': user, 'date': '2025-10-18', 'amount': 10000, 'payment_method': 'наличные'},]

        for pay in payments:
            payments, created = Payment.objects.get_or_create(**pay)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added payment: {pay['user']}'))
            else:
                self.stdout.write(self.style.WARNING(f'Payment already exists: {pay['user']}'))
