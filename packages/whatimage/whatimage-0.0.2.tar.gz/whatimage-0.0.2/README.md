# whatimage
Python library to detect image type from a few bytes

## Installation
pip install whatimage

## Usage
```python
import whatimage

with open('image.jpg', 'rb') as f:
    data = f.read()
fmt = whatimage.identify_image(data)
print(fmt)
```
> 'jpeg'

