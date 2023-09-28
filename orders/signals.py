from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot

from .models import Order, WaitingList


# Сигнал для события сохранения объекта Order
@receiver(post_save, sender=Order)
def post_save_order(sender, instance, **kwargs):
    serial = Robot.objects.filter(serial=instance.robot_serial).first()

    if not serial:
        
        # Создание объекта WaitingList, связанный с этим заказом, если робот не найден
        waiting = WaitingList.objects.create(order=instance)
        waiting.save()
