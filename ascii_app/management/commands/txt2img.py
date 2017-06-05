##
# manage.py command
# https://github.com/vano144/django_convert_ascii_service#txt2img
from ascii_app.ascii_converter.preprocess_image import PreprocessImageAPI
from ascii_app.utils import check_commands_arguments
from django.core.management.base import BaseCommand
import cv2


class Command(BaseCommand):
    help = 'Convert txt file to img'

    def add_arguments(self, parser):
        parser.add_argument('input_txt_path')
        parser.add_argument('output_img_path')

    def handle(self, *args, **options):
        input_txt_path = options['input_txt_path']
        output_img_path = options['output_img_path']
        check_commands_arguments(input_txt_path, output_img_path)
        result_img = PreprocessImageAPI.text_image(input_txt_path)
        result_img.save(output_img_path)
