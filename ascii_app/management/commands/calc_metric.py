##
# manage.py command
# https://github.com/vano144/django_convert_ascii_service#txt2img
from ascii_app.ascii_converter.metric import Metric
from ascii_app.utils import check_commands_arguments
from django.core.management.base import BaseCommand
import cv2


import imutils
class Command(BaseCommand):
    help = '0-Preprocess' \
           '1-Skelet' \
           '2-ASCII' \
           '3-Just comparing'

    def add_arguments(self, parser):
        parser.add_argument('original_path')
        parser.add_argument('ideal_path')
        parser.add_argument('mode')

    def handle(self, *args, **options):
        original_path = options['original_path']
        ideal_path = options['ideal_path']
        mode = int(options['mode'])
        if mode == 0:
            Metric.compare_img(original_path, ideal_path)
        elif mode == 1:
            Metric.compare_skeletonization(original_path, ideal_path)
        elif mode == 2:
            Metric.compare_ascii(original_path, ideal_path)
        elif mode == 3:
            Metric.compare_init_images(original_path, ideal_path)
        else:
            raise Exception("Not implemented mode")
        return 0

