from django.db import models
from time import timezone

# Create your models here.


##
# @class enum of ImageTypes
class ImageTypes:
    cv_img = "cv"
    pil_img = "pil"

    @classmethod
    def get_img_types(cls):
        return ImageTypes.cv_img, ImageTypes.pil_img


# class Content(models.Model):
#     download_time = models.DateTimeField(default=timezone.now)
#     image_path = models.TextField()
#     text_file_path = models.TextField()
