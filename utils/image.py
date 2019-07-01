"""Image manipulation functions go here"""

# Goal is for this to be file type agnostic (within reason) and then from there,
# figure out what the file is, process it accordingly and then save the thumbnail in the desired area.
# This should probably be asyncd because this shit will interrupt a fuck ton.

import os
from wand.image import Image
from subprocess import call


class Thumbify:
    """
    This will probably need access to specific things that I can't think of right now.
    usage: Thumbify(request/file)
    """

    def __init__(self, fo, filename=None):
        """
        init fname...
        """
        self.fo = fo
        self.fname = filename

    def create_thumb(self):
        """
        Resize to 250, then crop and from that do css
        bullshit to fix it.
        """
        path, ext = self.fname.rsplit(".")
        with Image(filename=self.fname) as original:
            with original.clone() as img:
                img.convert("jpeg")
                if img.height == img.width:
                    img.transform(resize="250x250")
                elif img.height > img.width:
                    img.transform(resize="250x")
                    img.crop(
                        0, int(round((img.height / 2) - 125)), width=250, height=250
                    )
                else:
                    img.transform(resize="x250")
                    img.crop(
                        int(round((img.width / 2) - 125)), 0, width=250, height=250
                    )

                try:
                    if os.path.basename(path).rsplit("_")[1] == "thumb":
                        img.save(filename=self.fname)
                except:
                    img.save(filename=f"{path}_thumb.jpg")
