# General useful utility functions for Python projects.

These are functions I use every day. Ideally they should make their way into the standard library.
I understand we cannot put everything in the standard library, hence this package. ;)

The various modules have the following requirements:

```
# util_email
imapclient
pyzmail

# util_fs
unidecode

# util_ftp
ftputil
paramiko

# util_image
pillow

# util_logging
logging_tree
```

If you only need one module it is recommended you install from source and manage the requirments yourself.


## Example usage:

```python
from PIL import Image

from lcutil import util_email as ue
from lcutil import util_image as ui

face = ui.scale_width(Image.open('face.jpg'), 100)
back = ui.scale_width(Image.open('back.jpg'), 100)

stiched = ui.stitch_vertical(face, back)
stiched.save('/tmp/stiched.jpg')

ue.html_email(from_='me <me@example.com>',
              to=['alice <alice@example.com>'],
              bcc=['bob <bob@example.com>'],
              subject='Here is an image for you',
              html_body='<html><body><h1>Hello World!</h1></body></html>',
              files=['/tmp/stiched.jpg'],
              smtp_server='smtp.example.com',
              smtp_port=25,
              smtp_username='username',
              smtp_password='password')
```
