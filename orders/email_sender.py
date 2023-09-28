from django.core.mail import send_mail


class EmailNotification:
    
    @staticmethod
    def send_robot_available_notification(customer_email, robot_model, robot_version):

        # Отправляем уведомление клиенту о доступности робота
        subject = "Робот доступен для заказа"
        message = (
            f"Добрый день!\n"
            f"Недавно вы интересовались нашим роботом модели {robot_model}, версии {robot_version}.\n"
            f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
            )
        from_email = "your@example.com"
        recipient_list = [customer_email]

        send_mail(subject, message, from_email, recipient_list)
        