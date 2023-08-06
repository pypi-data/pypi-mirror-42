# -*- coding: UTF-8 -*-
import os
from icv.core import errors
from PIL import Image


def show_image(image_path):
    assert os.path.exists(image_path),errors.IMAGE_PATH_NOT_EXISTS
    im = Image.open(image_path)
    im.show()