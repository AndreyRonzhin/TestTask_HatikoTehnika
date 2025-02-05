from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import telebot



class BaseModel(models.Model):
    objects = models.Manager()
    class Meta:
        abstract = True

class UserTgBot(BaseModel):
    user_id = models.PositiveIntegerField(primary_key=True, editable=False,  verbose_name="ID", )
    name = models.CharField(max_length=255, verbose_name="Имя")
    username = models.CharField(max_length=255, verbose_name="Имя пользователя")
    access_is_allowed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
        ]
        verbose_name = "Пользователь телеграмма"
        verbose_name_plural = "Пользователи телеграмма"


@receiver(post_save, sender=UserTgBot)
def post_save(sender, instance, **kwargs):
    if sender == UserTgBot:
        if instance.access_is_allowed:
            bot = telebot.TeleBot(settings.TOKEN_TG_BOT)
            bot.send_message(instance.user_id, "Вам разрешен доступ.")
            bot.send_message(instance.user_id, "Введите IMEI устройства.")