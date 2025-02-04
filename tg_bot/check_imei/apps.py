from django.apps import AppConfig


class CheckImeiConfig(AppConfig):
    verbose_name = "Проверка IMEI"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'check_imei'
