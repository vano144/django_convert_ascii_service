## Initialization

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

- `text`: JSON array of rectangles representing all text areas created by user
- `crop`: JSON object representing crop rectangle
- `image_type`: JSON string of image mime type
- `image`: binary image data

**Response**:

*Content-Type*: `application/json`

*Parameters*:

- `text`: UTF-8 text string of algo result (no html inside!)
- `image`: image url (either path or `data:image/png;base64,`-like)

