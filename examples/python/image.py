#!/usr/bin/python
# $Id: image.py,v 1.20 2012/09/13 14:26:21 rp Exp $
#
# PDFlib client: image example in Python
#

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

imagefile = "nesrin.jpg"

# This is where font/image/PDF input files live. Adjust as necessary.
searchpath = "F:\\PDFlib\\examples\\data"


p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    if p.begin_document("image.pdf", "") == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "image.py")
    p.set_info("Author", "Thomas Merz")
    p.set_info("Title", "image sample (Python)")

    image = p.load_image("auto", imagefile, "")
    if image == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    # dummy page size, will be adjusted by p.fit_image()
    p.begin_page_ext(10, 10, "")
    p.fit_image(image, 0, 0, "adjustpage")
    p.close_image(image)
    p.end_page_ext("")

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
