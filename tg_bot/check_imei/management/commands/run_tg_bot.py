from django.core.management import BaseCommand
from check_imei import server_tg_bot


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        server_tg_bot.start()
