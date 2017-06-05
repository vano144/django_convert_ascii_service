# django_convert_ascii_service


## Initialization static files

```bash
./loadlibs.sh [--force]
```

Run this to get all dependencies:

+ bootstrap
+ FileSaver.js
+ Pace.js

See all dependencies inside the script.

## API

### Process

**Request**

`POST api/process`

*Content-Type*: `multipart-form-data`

*Parameters*:

- `text`: JSON array of rectangles representing all text areas created by user, which will be deleted on server
- `crop`: JSON object representing crop rectangle, only its part will be transoform to ascii
- `image_type`: JSON string of image mime type
- `image`: binary image data

Example of json:


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

**Response**:

*Content-Type*: `application/json`

*Parameters*:

- `text`: UTF-8 text string of algorithm result (no html inside!)
- `image`: image url (either path or `data:image/png;base64,`-like)


## command line tools ##
