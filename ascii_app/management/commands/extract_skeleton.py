##
# manage.py command
# TODO: link to doc
from ascii_app.ascii_converter.helpers import process_image
from ascii_app.ascii_converter.helpers import skeletonization
from ascii_app.utils import check_commands_arguments
from django.core.management.base import BaseCommand
import cv2


class Command(BaseCommand):
    help = 'Extract skeleton from image'

    def add_arguments(self, parser):
        parser.add_argument('input_img_path')
        parser.add_argument('output_img_path')

    def handle(self, *args, **options):
        input_img_path = options['input_img_path']
        output_img_path = options['output_img_path']
        check_commands_arguments(input_img_path, output_img_path)
        input_img = cv2.imread(input_img_path, 0)
        processed_img = process_image(input_img)
        result_img, _ = skeletonization(processed_img)
        cv2.imwrite(output_img_path, result_img)
