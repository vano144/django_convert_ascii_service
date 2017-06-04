##
# manage.py command
# TODO: link to doc
from ascii_app.ascii_converter.text_search import TextSearcher
from ascii_app.utils import check_commands_arguments, get_extension_by_filename
from ascii_app.ascii_converter.utils import get_tmp_file_name
from PIL import Image
from django.core.management.base import BaseCommand
import cv2


class Command(BaseCommand):
    help = 'Show possible areas with text'

    def add_arguments(self, parser):
        parser.add_argument('input_img_path')
        parser.add_argument('--save',
                            action='store_true',
                            dest='save',
                            default=False,
                            help='Only save result, path will be displayed')

    def handle(self, *args, **options):
        input_img_path = options['input_img_path']
        check_commands_arguments(input_img_path)
        input_img = cv2.imread(input_img_path, 1)
        extension = get_extension_by_filename(input_img_path)
        if extension.startswith("."):
            extension = extension[1:]
        txt_searcher = TextSearcher(input_img)
        txt_searcher.set_width_and_height_metric()
        txt_searcher.find_and_delete_text(extension=extension)
        if options["save"]:
            tmp_img_filename = get_tmp_file_name(extension=extension)
            Image.fromarray(txt_searcher.output).save(tmp_img_filename)
            return tmp_img_filename
        else:
            Image.fromarray(txt_searcher.output).show()

