# django_convert_ascii_service

## API ##

### api/process ###

ONLY *POST* request.
 Convert image to ascii. input arguments json with fields:
 
 * text - array of dicts, representing an areas to be deleted from image
 * crop - dict, representing an area to be croped from image 
 * image_type - image's type
 
 and image, json example:

      {
        "text": [
          {
            "x": 19,
            "y": 131.8125,
            "width": 79,
            "height": 48.1875
          },
          {
            "x": 17,
            "y": 20.8125,
            "width": 73,
            "height": 63.1875
          }
        ],
        "crop": {
          "x": 13,
          "y": 11.8125,
          "width": 104,
          "height": 103.1875
        },
        "image_type": "image/png"
      }
 
 It should be send with Content-type multipart/form-data and suitable boundary. 
 Returns converted image to ascii in sting and image of this. Example of response:
 
     {
      "image": "data:image/png;base64, ...",
      "text": ...
     }

## command line tools ##
