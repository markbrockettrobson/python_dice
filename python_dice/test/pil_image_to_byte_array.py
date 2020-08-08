import io

import PIL.Image as Image


def image_to_byte_array(image: Image) -> bytes:
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format="TIFF")
    return img_byte_array.getvalue()
