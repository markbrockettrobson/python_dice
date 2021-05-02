import os
import sys


def get_image_path(image_name: str):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "windows" if sys.platform.startswith("win") else "linux",
        image_name,
    )
