# imshowtools

This library that allows you to view images in Jupyter notebooks in a much simpler way.

## Installation

To install imshowtools,

```
pip install imshowtools
```

## Usage

### Single Image

To show a single image
```
from imshowtools import *
imshow(your_image)
```

### Multiple Images

To show multiple images
```
from imshowtools import *
imshow(image_1, image_2, image_3)
```

### Namespaces
If you do not want to use `imshow` directly in your app (maybe you have another function named imshow), you shall use it like

```
import imshowtools
imshowtools.imshow(your_image)
```