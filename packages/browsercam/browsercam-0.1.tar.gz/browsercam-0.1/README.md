# browsercam

This module was built for Chromebooks running Crostini, which currently
don't have access to the webcam module. Using browsercam is simple:

```python
import browsercam

def process_image(image):
    size = len(image)
    print('Captured image is {} bytes'.format(isize))

webcam = browsercam.Webcam()
webcam.on_capture(process_image)
webcam.start()
```
