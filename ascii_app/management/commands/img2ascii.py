##
# manage.py command
# https://github.com/vano144/django_convert_ascii_service#img2ascii
from ascii_app.ascii_converter.helpers import convert_image_to_ascii
from ascii_app.utils import check_commands_arguments
from django.core.management.base import BaseCommand
import cv2
from optparse import make_option


class Command(BaseCommand):
    help = 'Extract skeleton from image'

    def add_arguments(self, parser):
        parser.add_argument('input_img_path')
        parser.add_argument('output_txt_path')
        parser.add_argument('--to_console',
                            action='store_true',
                            dest='output',
                            default=False,
                            help='Output in console too')

    def handle(self, *args, **options):
        input_img_path = options['input_img_path']
        output_txt_path = options['output_txt_path']
        check_commands_arguments(input_img_path, output_txt_path)
        img = cv2.imread(input_img_path, 0)
        _, _ = convert_image_to_ascii(img, file_name=output_txt_path, to_console=options["output"])
        return "Result is here: %s" % output_txt_path
