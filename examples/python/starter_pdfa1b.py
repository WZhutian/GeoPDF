#!/usr/bin/python
# $Id: starter_pdfa1b.py,v 1.4 2012/09/13 14:26:21 rp Exp $
#
# PDF/A-1b starter:
# Create PDF/A-1b conforming output
#
# required software: PDFlib/PDFlib+PDI/PPS 9
# required data: font file, image file

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "../data"
imagefile = "nesrin.jpg"
outfilename = "starter_pdfa1b.pdf"

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    # PDF/A-1a requires Tagged PDF
    if (p.begin_document(outfilename, "pdfa=PDF/A-1b:2005") == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    #
    # We use sRGB as output intent since it allows the color
    # spaces CIELab, ICC-based, grayscale, and RGB.
    #
    # If you need CMYK color you must use a CMYK output profile.


    p.load_iccprofile("sRGB", "usage=outputintent")

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_pdfa1b")

    p.begin_page_ext(595, 842, "")

    # font embedding is required for PDF/A
    font = p.load_font("LuciduxSans-Oblique", "unicode", "embedding")
    if font == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.setfont(font, 24)

    p.fit_textline("PDF/A-1b:2005 starter", 50, 700, "")

    # We can use an RGB image since we already supplied an
    # output intent profile.

    image = p.load_image("auto", imagefile, "")
    if (image == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    # Place the image at the bottom of the page
    p.fit_image(image, 0.0, 0.0, "scale=0.5")

    p.end_page_ext("")
    p.close_image(image)

    p.end_document("")

except PDFlibException:
    print("PDFlib exception occurred:\n[%d] %s: %s" %
	((p.get_errnum()), p.get_apiname(),  p.get_errmsg()))
    print_tb(exc_info()[2])

except Exception:
    print("Exception occurred: %s" % (exc_info()[0]))
    print_tb(exc_info()[2])

finally:
    p.delete()
