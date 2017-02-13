#!/usr/bin/python
# -*- coding: utf-8 -*-
# $Id: starter_basic.py,v 1.8.2.1 2013/07/05 11:26:46 rp Exp $
#
# Basic starter:
# Create some simple text, vector graphics and image output
#
# required software: PDFlib/PDFlib+PDI/PPS 9
# required data: none
#

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "../data/"
imagefile = "nesrin.jpg"
outfilename = "starter_basic.pdf"

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    if (p.begin_document(outfilename, "") == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_basic")

    # We load the image before the first page, and use it
    # on all pages

    image = p.load_image("auto", imagefile, "")
    if (image == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    # Page 1
    p.begin_page_ext(595, 842, "")

    # use LinLibertine_R font with text format UTF-8 for placing the text
    # and demonstrate various options how to pass the UTF-8 text to PDFlib
    #
    optlist = "fontname={LinLibertine_R} embedding fontsize=24 encoding=unicode"

    # plain ASCII text */
    p.fit_textline("en: Hello!", 50, 700, optlist)
    # using pythons unicode notation */
    p.fit_textline(u"gr: \u0393\u03B5\u03B9\u03AC!", 50, 650, optlist);
    # plain UTF-8 text */
    p.fit_textline(u"ru: Привет!", 50, 600, optlist)
    # using PDFlib's character references */
    p.fit_textline("es: &#xA1;Hola!", 50, 550, optlist + " charref=true");


    p.fit_image(image, 0.0, 0.0, "scale=0.25")

    p.end_page_ext("")

    # Page 2
    p.begin_page_ext(595, 842, "")

    # red rectangle
    p.setcolor("fill", "rgb", 1.0, 0.0, 0.0, 0.0)
    p.rect(200, 200, 250, 150)
    p.fill()

    # blue circle
    p.setcolor("fill", "rgb", 0.0, 0.0, 1.0, 0.0)
    p.arc(400, 600, 100, 0, 360)
    p.fill()

    # thick gray line
    p.setcolor("stroke", "gray", 0.5, 0.0, 0.0, 0.0)
    p.setlinewidth(10)
    p.moveto(100, 500)
    p.lineto(300, 700)
    p.stroke()

    # Using the same image handle means the data will be copied
    # to the PDF only once, which saves space.

    p.fit_image(image, 150.0, 25.0, "scale=0.25")
    p.end_page_ext("")

    # Page 3
    p.begin_page_ext(595, 842, "")

    # Fit the image to a box of predefined size (without distortion)
    optlist = "boxsize={400 400} position={center} fitmethod=meet"
    p.fit_image(image, 100, 200, optlist)

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
