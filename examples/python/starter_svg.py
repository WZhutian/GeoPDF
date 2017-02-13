#!/usr/bin/python
# Id: starter_svg.py,v 1.1 2013/01/22 21:35:50 rjs Exp 
#
# Starter SVG:
# Load SVG graphics and fit into a box
#
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: SVG graphics


searchpath = "../data"
outfile = "starter_svg.pdf"

graphicsfile = "PDFlib-logo.svg"
x = 100
y = 300
boxwidth = 400
boxheight = 400

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# create a new PDFlib object
p = PDFlib()

try:

    p.set_option("SearchPath={{" + searchpath + "}}")

    # This means we must check return values of load_graphics() etc.
    p.set_option("errorpolicy=return")

    if  p.begin_document(outfile, "") == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_svg")

    # Load the graphics
    graphics = p.load_graphics("auto", graphicsfile, "")
    if graphics == -1:
        raise PDFlibException("Error: " + p.get_errmsg())


    p.begin_page_ext(0, 0, "width=a4.width height=a4.height")

    # ------------------------------------------------------
    # Fit the graphics into a box with proportional resizing
    # ------------------------------------------------------

    # The "boxsize" option defines a box with a given width and height
    # and its lower left corner located at the reference point.
    # "position={center}" positions the graphics in the center of the
    # box.
    # "fitmethod=meet" resizes the graphics proportionally until its
    # height or width completely fits into the box.
    # The "showborder" option is used to illustrate the borders of the
    # box

    optlist = ("boxsize={ %d %d } position={center} fitmethod=meet "
		"showborder" % (boxwidth, boxheight))

    # Before actually fitting the graphics we check whether fitting is
    # possible.

    if p.info_graphics(graphics, "fittingpossible", optlist) == 1:
        p.fit_graphics(graphics, x, y, optlist)
    else:
        raise PDFlibException("Cannot place graphics:" + p.get_errmsg())

    p.end_page_ext("")

    p.close_graphics(graphics)


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
