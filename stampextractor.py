import sys
import os
import subprocess

from PIL import Image


def pdf_to_jpg(pdf):

    # Cf this discussion http://stackoverflow.com/questions/6605006/convert-pdf-to-image-with-high-resolution

    name, _ = os.path.splitext(pdf)
    jpg = "%s.jpg" % name

    args = [
        "convert",
        "-density",
        "300",
        "-trim",
        pdf,
        "-quality",
        "100",
        "-sharpen",
        "0x1.0",
        jpg
    ]

    subprocess.check_output(args)
    return jpg


if __name__ == "__main__":

    try:
        stamp_board_file = sys.argv[1]
    except IndexError:
        print "You should specify a stamp board file"
        sys.exit()

    try:
        jpg = pdf_to_jpg(stamp_board_file)
        stamp_board = Image.open(jpg)
    except IOError as e:
        print e
        print "Could not find stamp board file ./boards/%s" % stamp_board_file
        sys.exit()

    (board_height, board_width) = stamp_board.size
    stroke_width = 1
    margin_x = 77
    margin_y = 75
    stamp_height = 373
    stamp_width = 700

    # Stamp boards layout is 21 63,5 x 38,1 mm
    for x in range(0, 3):
        for y in range(0, 7):

            # extract individual stamps
            left = x * stamp_width + x * margin_x + 2 * (x + 1) * stroke_width
            top = y * stamp_height + y * margin_y + 2 * (y + 1) * stroke_width
            right = left + stamp_width
            bottom = top + stamp_height
            cropped = stamp_board.crop((left, top, right, bottom))

            # extract barcode only
            left = 437
            top = 68
            right = left + 216
            bottom = top + 216

            bar_code = cropped.crop((left, top, right, bottom))

            (filename, extension) = os.path.splitext(jpg)
            stamp_filename = "./stamps/%s_%s%s%s" % (os.path.basename(filename), x + 1, y + 1, extension)
            bar_code.save(stamp_filename)












