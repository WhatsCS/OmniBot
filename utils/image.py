"""Image manipulation functions go here"""

# TODO: Get this working using byte blobs so we can keep everything in memory and never have to save (ideally)
# This should probably be asyncd because this shit will interrupt a fuck ton.

from wand.image import Image


def create_thumb(fobject=None):
    """
    Resize to 250, then crop and from that do css
    bullshit to fix it.
    """
    with Image(blob=fobject) as img:
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
        fobject = img.make_blob('jpg')
        return fobject


# def create_montage(img_list):
#     # `$ montage test*.jpg -tile 3x3 -geometry +0+0 montage-test.jpg`
#     pass
