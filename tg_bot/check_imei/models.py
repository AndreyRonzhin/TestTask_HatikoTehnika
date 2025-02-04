from django.db import models

class BaseModel(models.Model):
    objects = models.Manager()
    class Meta:
        abstract = True

class UserTgBot(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Имя")
    username = models.CharField(max_length=255, verbose_name="Имя пользователя")
    user_id = models.CharField(max_length=15, verbose_name="ID", )
    access_is_allowed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
        ]
        verbose_name = "Пользователь телеграмма"
        verbose_name_plural = "Пользователи телеграмма"


