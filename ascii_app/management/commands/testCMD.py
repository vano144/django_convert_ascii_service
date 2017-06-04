##
# manage.sh command
# https://github.com/Visyond/v5#add_email
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'test'

    def add_arguments(self, parser):
        parser.add_argument('first_arg')

    def handle(self, *args, **options):
        first_arg = options['first_arg']
        print(first_arg)


