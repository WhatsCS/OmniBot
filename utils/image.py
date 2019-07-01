"""Image manipulation functions go here"""

# TODO: Get this working using byte blobs so we can keep everything in memory and never have to save (ideally)
# This should probably be asyncd because this shit will interrupt a fuck ton.

import os
from wand.image import Image
from subprocess import call
import aiohttp


def create_thumb(self, fobject=None, flist=None):
    """
    Resize to 250, then crop and from that do css
    bullshit to fix it.
    """

    with Image(filename=self.fo) as original:
        with original.clone() as img:
            img.convert("jpeg")
            if img.height == img.width:
                img.transform(resize="150x150")
            elif img.height > img.width:
                img.transform(resize="150x")
                img.crop(
                    0, int(round((img.height / 2) - 225)), width=150, height=150
                )
            else:
                img.crop(
                    int(round((img.width / 2) - 225)), 0, width=150, height=150
                )
                img.transform(resize="x150")


def create_montage(self, img_list):
    # `$ montage test*.jpg -tile 3x3 -geometry +0+0 montage-test.jpg`
    pass
