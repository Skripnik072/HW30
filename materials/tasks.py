from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone

from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from materials.models import Course
from users.models import User, Subscription


@shared_task
def send_update(course_id):
    # Внутри задачи проверяем, прошло ли более 4 часов с последнего обновления курса

    '''Получаем курсы и пользователей'''
    course = Course.objects.get(id=course_id)
    users = User.objects.all()

    '''Получаем подписки на курсы'''
    for user in users:
        subs_item = Subscription.objects.filter(course_id=course_id, user=user.pk).first()
        if subs_item:
            if datetime.now() - course.last_updated >= timedelta(hours=4):
                # Отправляем уведомление пользователю
                send_mail(
                    subject="Отчет по обновлению курса",
                    message=f"Курс {course} обновлен",
                    from_email=settings / EMAIL_HOST_USER,
                    recipient_list=[user.email])
                # Здесь логика отправки письма
                print(f"Отправлено уведомление для курса {course_id}")
            else:
                print("Прошло менее 4 часов, уведомление не отправлено.")


@shared_task
def deactivate_users():
    '''Деактивируем пользователя, который не заходил более 30 дней'''
    termination_date = timezone.now() - timedelta(days=30)
    users_list = User.objects.filter(last_login__isnull=False, last_login__lt=termination_date, is_active=True)
    for user in users_list:
        user.is_active = False
        user.save()
        print(f'Пользователь {user.email} заблокирован')
    print("Задача выполнена")
