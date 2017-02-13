#!/usr/bin/python
# $Id: starter_pdfx3.py,v 1.4 2012/09/13 14:26:21 rp Exp $
#
# PDF/X-3 starter:
# Create PDF/X-3 conforming output
#
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: font file, image file, icc profile
#                (see www.pdflib.com for ICC profiles)

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

def printf(format, *args):
    sys.stdout.write(format % args)

# This is where the data files are. Adjust as necessary.*/
searchpath = "../data"
imagefile = "nesrin.jpg"
outfilename = "starter_pdfx3.pdf"

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    if (p.begin_document(outfilename, "pdfx=PDF/X-3:2003") == 0):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_pdfx3")

    # You can use one of the Standard output intents (e.g. for SWOP
    # printing) which do not require an ICC profile:
    #
    # p.load_iccprofile("CGATS TR 001", "usage=outputintent")
    #
    # However, if you use ICC or Lab color you must load an ICC
    # profile as output intent:
    if (p.load_iccprofile("ISOcoated.icc", "usage=outputintent") == -1):
        printf("Error: %s\n", p.get_errmsg())
        printf("Please install the ICC profile package from " +
            "www.pdflib.com to run the PDF/X starter sample.\n")
        exit(2);


    p.begin_page_ext(595, 842, "")

    # font embedding is required for PDF/X
    font = p.load_font("LuciduxSans-Oblique", "unicode", "embedding")
    if font == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.setfont(font, 24)

    spot = p.makespotcolor("PANTONE 123 C")
    p.setcolor("fill", "spot", spot, 1.0, 0.0, 0.0)
    p.fit_textline("PDF/X-3:2003 starter", 50, 700, "")

    # The RGB image below needs an icc profile; we use sRGB.
    icc = p.load_iccprofile("sRGB", "")
    image = p.load_image("auto", imagefile, "iccprofile=" + repr(icc))

    if (image == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.fit_image(image, 0.0, 0.0, "scale=0.5")

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
