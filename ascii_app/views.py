from .decorators import set_json, rest_api_call, handle_errors, set_json1
from .utils import crop_image, convert_pil_image_to_b64, obtain_img_from_client, convert_to_ascii
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from PIL import Image
# Create your views here.


@csrf_exempt
@handle_errors
@set_json1
@rest_api_call
def convert_to_ascii_view(request):
    if request.method == "POST" and hasattr(request, "json_data") \
            and hasattr(request, "FILES") and len(request.FILES) > 0:
        img, image_type, image_extension = obtain_img_from_client(request)
        if "crop" in request.json_data:
            img = crop_image(img, request.json_data["crop"])
        img, text = convert_to_ascii(img)
        result = {
            "image": convert_pil_image_to_b64(img, image_extension, image_type),
            "text": text
        }
        return result


@csrf_exempt
@handle_errors
@rest_api_call
def test(request):
    return {
        "test": 4
    }


@csrf_exempt
def main_page(request):
    return render(request, 'index.html', locals())