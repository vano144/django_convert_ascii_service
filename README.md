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


## command line tools

### extract_skeleton

      python3 manage.py extract_skeleton <input_img_path> <output_img_path>
      
  Extract skeleton from image to image, which is located by `output_img_path`

### img2ascii

      python3 manage.py img2ascii <input_img_path> <output_txt_path> [--to_console]
  
  Convert image to ascii ans save it in txt file by path `output_txt_path`. Apart from it, this cmd tools allow you to output result in console by giving to cmd special file.

### pre_process

      python3 manage.py pre_process <input_img_path> <output_img_path>
      
  Apply preprocess on image and save result to `output_img_path`

### search_text
      
      python3 manage.py search_text <input_img_path> [--save]
      
  Search and highlight (in future delete) areas with texts. In case of passing extra argument, this cmd tool only save it to filepath, which will be displayed after the end of program.

### txt2img

      python3 manage.py txt2img <input_txt_path> <output_img_path>
  
  Convert txt file to image 
