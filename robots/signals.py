from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.email_sender import EmailNotification
from orders.models import WaitingList

from .models import Robot


# СИгнал для события сохранения объекта Robot
@receiver(post_save, sender=Robot)
def robot_availability_signal(sender, instance, **kwargs):

    serial = instance.serial
    model = instance.model
    version = instance.version

    # Проверка, есть ли ожидающий заказ с указанным серийным номером робота
    waiting_list = WaitingList.objects.filter(order__robot_serial=serial).first()

    if waiting_list:
        email = waiting_list.order.customer.email
        # Отправляем уведомление о доступности робота клиенту
        EmailNotification.send_robot_available_notification(email, model, version)
        
        waiting_list.delete()

