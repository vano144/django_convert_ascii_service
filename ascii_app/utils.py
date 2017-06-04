import tempfile
import cv2
import base64
import mimetypes
import io
import os
from PIL import Image
import numpy as np
from .models import ImageTypes
from .ascii_converter import PreprocessImageAPI
from .ascii_converter.helpers import convert_image_to_ascii
from .ascii_converter.utils import content_to_tmp_file


##
# Return cv2 image by using tmp file
# @param img_in_bytes image in bytes
# @param extension extension of image
# @param way color type of a loaded image - int
# @return image as a numpy.ndarray
def get_cv_image_file(img_in_bytes, extension, way=0):
    tmp_file_name = content_to_tmp_file(img_in_bytes, extension=extension)
    return cv2.imread(tmp_file_name, way)


##
# Return cv2 image by using PIL
# @param img_in_bytes image in bytes
# @return image as a numpy.ndarray
def get_cv_image(image_io_bytes):
    img = Image.open(image_io_bytes)
    img = np.array(img.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


##
# Crop image by type
# @param img
# @param rectangle dict with fields: x, y, width, height
# @param img_type type of image from enum @ImageTypes
# @return cropped cv2 img in ndarray
# @error Exception("unknown image's type")
def crop_image(img, rectangle, img_type=ImageTypes.cv_img):
    assert img_type in ImageTypes.get_img_types()
    if img_type == ImageTypes.cv_img:
        return PreprocessImageAPI.crop_cv_image(img, rectangle)
    elif img_type == ImageTypes.pil_img:
        return PreprocessImageAPI.crop_pil_image(img, rectangle)
    raise Exception("unknown image's type")


##
# Convert cv2 image to base64
# @param img cv2 image
# @param image_extension images'extension
# @return base 64 str
def get_base64_image(img, image_extension):
    img_bytes = (cv2.imencode('.%s' % image_extension, img)[1]).encode("utf-8")
    return base64.b64encode(img_bytes).decode("utf-8")


##
# Get extension by image type
# @param image_type type in str, ex: image/png
# @return extension in str or None ex: png
def get_extension(image_type):
    try:
        return mimetypes.guess_extension(image_type)
    except:
        return None


##
# Get extension by image type
# @param image_type type in str, ex: image/png
# @return extension in str or None ex: png
def get_extension_by_filename(filename):
    try:
        return mimetypes.guess_extension(mimetypes.guess_type(filename)[0])
    except:
        return None


##
# Get type of image according to image's filename
# @param filename image's filename
# @return type of image or none, ex: image/png
def get_type(filename):
    try:
        return mimetypes.guess_type(filename)[0]
    except:
        return None


##
# Get cv image from client with extension ant type
# @param request django's @HttpRequest
# @return cv image, image's type and image's extension
def obtain_img_from_client(request):
    image_type = request.json_data["image_type"]
    image_extension = get_extension(image_type)
    assert image_extension is not None
    img = get_cv_image(request.FILES['image'])
    return img, image_type, image_extension


##
# Convert cv image to ascii symbols and return result in text and image
# @param img cv image
# @return img and text
def convert_to_ascii(img):
    return convert_image_to_ascii(img=img)


##
# Convert b64 img from client to cv image
# @param b64_image_in_str b64 image in str
# @return cv img
def get_base64_img(b64_image_in_str):
    split_b64_img = b64_image_in_str.split("base64,")
    img_content_bytes = base64.b64decode(split_b64_img[-1].encode('utf-8'))
    return get_cv_image(img_content_bytes)


##
# Convert image to str like: image type;base64,img_in_b64
# @param img pil image
# @param image_extension extension image
# @param image_type image's type
# @return str like: image type;base64,img_in_b64
def convert_pil_image_to_b64(img, image_extension, image_type):
    img_byte_arr = io.BytesIO()
    try:
        img.save(img_byte_arr, format=image_extension.split(".")[-1])
    except:
        img.save(img_byte_arr, format="png")
    return "data:" + image_type + ";base64," + base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")


##
# Check input arguments (input_img_path, output_img_path) and return cv image according to input_img_path
# @param input_path input path in str
# @param output_path output path in str
# @error AssertionError, Exception Bad input_path
def check_commands_arguments(input_path, output_path=None):
    assert input_path
    if output_path is not None:
        assert output_path
    if not os.path.exists(input_path):
        raise Exception("Bad input_img_path")

#        ––––––\                       /
#               *\                     ⎪
#                 **\                  ⎪
#                    *\                ⎪
#                      **\             ⎪
#                         *\\          ⎪
#                           **         ⎪
#                             \        ⎪
#                              \       ⎪
#                               /\     ⎪
#                                 \    ⎪
#                                  /   ⎪
#                                  \   ⎪
#                                   *  ⎪
#                                   \  ⎪
#                                    * ⎪                /–––––––––
# ––––––––––––––\                    * ⎪      /–––––––––          \––––––––
#                –––––––\       ––––⎪–– ––––––                             \–––––
#                        ––––––/   *⎪  ⎪
#                                 /    ⎪
#                                 *    ⎪
#                                /     ⎪
#                                *     ⎪
#                              **      ⎪
#                            */        ⎪
#                          */          ⎪
#                        */            ⎪
#                      */              ⎪
#                    **                ⎪
#                 **/                  ⎪
#              **/                     ⎪
#     ––––––––/                        ⎪
#                                      ⎪
#                                      ⎪
