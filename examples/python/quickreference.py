#!/usr/bin/python
# $Id: quickreference.py,v 1.21 2012/09/13 14:26:21 rp Exp $
#
# PDFlib/PDI client: mini imposition demo
#

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

maxrow = 2
maxcol = 2
width = 500.0
height = 770.0

infile = "reference.pdf"
searchpath = "../data"

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    if p.begin_document("quickreference.pdf", "") == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "quickreference.py")
    p.set_info("Author", "Thomas Merz")
    p.set_info("Title", "mini imposition demo (Python)")

    manual = p.open_pdi_document(infile, "")
    if manual == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    row = 0
    col = 0

    endpage = int(p.pcos_get_number(manual, "length:pages"))

    for pageno in range(1, endpage+1):
        if row == 0 and col == 0:
            p.begin_page_ext(width, height, "topdown")
            font = p.load_font("Helvetica-Bold", "unicode", "")
            if font == -1:
                raise PDFlibException("Error: " + p.get_errmsg())
            p.setfont(font, 18)
            p.set_text_pos(24, 24)
            p.show("PDFlib Quick Reference")

        page = p.open_pdi_page(manual, pageno, "")

        if page == -1:
            raise PDFlibException("Error: " + p.get_errmsg())

        optlist = "scale " + repr(1.0/maxrow)

        p.fit_pdi_page(page,
                width/maxcol*col, (row + 1) * height/maxrow, optlist)
        p.close_pdi_page(page)

        col = col+1
        if col == maxcol:
            col = 0
            row = row+1

        if row == maxrow:
            row = 0
            p.end_page_ext("")

    # finish the last partial page
    if row != 0 or col != 0:
        p.end_page_ext("")

    p.end_document("")
    p.close_pdi_document(manual)

except PDFlibException:
    print("PDFlib exception occurred:\n[%d] %s: %s" %
	((p.get_errnum()), p.get_apiname(),  p.get_errmsg()))
    print_tb(exc_info()[2])

except Exception:
    print("Exception occurred: %s" % (exc_info()[0]))
    print_tb(exc_info()[2])

finally:
    p.delete()
