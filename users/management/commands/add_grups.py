from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Добавление групп пользователей в БД'

    def handle(self, *args, **options):
        "Создаем группу"
        moderators_group, _ = Group.objects.get_or_create(name='Moderators')
        "Получаем разрешения для группы"
        add_perm_lesson = Permission.objects.get(codename='add_lesson')
        change_perm_lesson = Permission.objects.get(codename='change_lesson')
        add_perm_course = Permission.objects.get(codename='add_course')
        change_perm_course = Permission.objects.get(codename='change_course')
        "Назначаем разрешения группе"
        moderators_group.permissions.add(add_perm_lesson, change_perm_lesson, add_perm_course, change_perm_course)
        permiss = [add_perm_lesson, change_perm_lesson, add_perm_course, change_perm_course]

        for perm in permiss:
            group, created = Group.objects.get_or_create(**perm)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added group'))
            else:
                self.stdout.write(self.style.WARNING(f'Group already exists'))