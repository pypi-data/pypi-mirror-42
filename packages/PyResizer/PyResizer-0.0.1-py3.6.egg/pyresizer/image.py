"""
    PyResizer
    ~~~~~~~~~

    https://github.com/jedie/PyResizer/
    https://pypi.org/project/PyResizer/

    created 2019 by Jens Diemer
    GNU General Public License v3 or later (GPLv3+)
"""
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as err:
    print("ERROR: %s" % err)
    print("Install https://python-pillow.org/ !")
    print("pip install Pillow")
    sys.exit(-1)


def convert(
    *,
    file_path,
    out_prefix,
    overwrite_existing=False,
    size=(1000, 1000),
    font_path=None,
    text=None,
    text_opacity=50,
    max_size=None,
    quality=95,
    quality_steps=5
):

    assert file_path.is_file(), "File not found: %s" % file_path

    out_filepath = Path(file_path.parent, "%s%s.jpg" % (file_path.stem, out_prefix))
    if out_filepath.is_file():
        print("Out file already exists: %s" % out_filepath)
        if not overwrite_existing:
            return

    im = Image.open(str(file_path))
    print("Image info keys:", im.info.keys())

    exif = im.info.get("exif", b"")
    if exif:
        print("Transfer origin EXIF")
    else:
        print("No EXIF data")

    icc_profile = im.info.get("icc_profile")
    if icc_profile:
        print("ICC Profile exists.")
    else:
        print("No ICC Profile.")

    im.thumbnail(size, Image.LANCZOS)

    if font_path and text:
        im = im.convert("RGBA")

        # make a blank image for the text, initialized to transparent text color
        txt_white = Image.new("RGBA", im.size, (255, 255, 255, 0))
        txt_black = Image.new("RGBA", im.size, (0, 0, 0, 0))

        font_size = int(round((size[0] * 0.015)))

        # get a font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception as err:
            print("ERROR loading %r: %s" % (font_path, err))
            print("Use default font")
            font = ImageFont.load_default()

        text_size = font.getsize("%s  " % text)

        # get a drawing context
        image_draw_white = ImageDraw.Draw(txt_white)
        image_draw_black = ImageDraw.Draw(txt_black)

        # draw text
        opacity = int(round(256 * text_opacity / 100))
        x = int(round(im.size[0] - text_size[0]))
        y = int(round(im.size[1] - (font_size * 2)))
        text_position = (x, y)
        print("Text position:", text_position)
        image_draw_white.text(text_position, text, font=font, fill=(255, 255, 255, opacity))

        text_position = (x + 1, y + 1)
        image_draw_black.text(text_position, text, font=font, fill=(0, 0, 0, opacity))

        im = Image.alpha_composite(im, txt_black)
        im = Image.alpha_composite(im, txt_white)

        im = im.convert("RGB")

    # im.show()

    while True:
        im.save(
            str(out_filepath),
            #
            # # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg
            "JPEG",
            #
            # preserve existing ICC profile:
            icc_profile=icc_profile,
            #
            # preserve existing EXIF data:
            exif=exif,
            #
            # encoder should make an extra pass over the image in order to select optimal encoder settings:
            optimize=True,
            #
            # image quality, on a scale from 1 (worst) to 95 (best). The default is 75. Values above 95 should be avoided
            quality=quality,
        )
        if not max_size:
            break

        file_size = out_filepath.stat().st_size
        print("Saved with %i%% -> %i Bytes" % (quality, file_size))

        if file_size > max_size:
            quality -= quality_steps
            print("Out size to big: try with %i%%" % quality)
        else:
            break
