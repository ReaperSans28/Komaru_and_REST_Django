from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from celery import shared_task
from education.models import Course, Subscription
from users.models import User
from django.conf import settings

@shared_task
def update_course(course_pk):
    course = Course.objects.filter(pk=course_pk).first()
    if not course:
        print(f'Курс с ID {course_pk} не найден.')
    subscriptions = Subscription.objects.filter(course=course_pk).select_related('user')
    for subscription in subscriptions:
        user = subscription.user
        send_mail(
            subject=f'Обновление курса "{course.title}"',
            message=f'Добрый день, {user.username}, курс "{course.title}" обновился.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        print(f'Уведомление отправлено на почту: {user.email}')

@shared_task
def check_last_login():
    users = User.objects.filter(last_login__isnull=False)
    for user in users:
        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'{user.email} - забанен.')
        else:
            print(f'{user.email} - доступен.')
