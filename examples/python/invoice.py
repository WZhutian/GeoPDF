#!/usr/bin/python
# $Id: invoice.py,v 1.19 2012/09/13 14:26:21 rp Exp $
#
# PDFlib client: invoice generation demo
#

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *
import time

infile = "stationery.pdf"

# This is where font/image/PDF input files live. Adjust as necessary.
searchpath = "../data"

left = 55
right = 530
fontsize = 12
pagewidth = 595
pageheight = 842
baseopt = \
        "ruler        {   30 45     275   375   475} " +\
        "tabalignment {right left right right right} " +\
        "hortabmethod ruler fontsize 12 "

closingtext = \
    "Terms of payment: <fillcolor={rgb 1 0 0}>30 days net. " +\
    "<fillcolor={gray 0}>90 days warranty starting at the day of sale. " +\
    "This warranty covers defects in workmanship only. " +\
    "<fontname=Helvetica-BoldOblique encoding=host>Kraxi Systems, Inc. " +\
    "<resetfont>will, at its option, repair or replace the " +\
    "product under the warranty. This warranty is not transferable. " +\
    "No returns or exchanges will be accepted for wet products."

data_name = [
 "Super Kite",
 "Turbo Flyer",
 "Giga Trash",
 "Bare Bone Kit",
 "Nitty Gritty",
 "Pretty Dark Flyer",
 "Free Gift" ]
data_price = [ 20, 40, 180, 50, 20, 75, 0]
data_quantity = [ 2, 5, 1, 3, 10, 1, 1]


ARTICLECOUNT = 6

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    if p.begin_document("invoice.pdf", "") == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "invoice.py")
    p.set_info("Author", "Thomas Merz")
    p.set_info("Title", "PDFlib invoice generation demo (Python)")

    stationery = p.open_pdi_document(infile, "")
    if stationery == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    page = p.open_pdi_page(stationery, 1, "")
    if page == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    boldfont = p.load_font("Helvetica-Bold", "unicode", "")
    if boldfont == -1:
        raise PDFlibException("Error: " + p.get_errmsg())
    regularfont = p.load_font("Helvetica", "unicode", "")
    if regularfont == -1:
        raise PDFlibException("Error: " + p.get_errmsg())
    leading = fontsize + 2

    # Establish coordinates with the origin in the upper left corner.
    p.begin_page_ext(pagewidth, pageheight, "topdown")

    p.fit_pdi_page(page, 0, pageheight, "")
    p.close_pdi_page(page)

    p.setfont(regularfont, fontsize)

    # Print the address
    y = 170
    p.set_text_option("leading=" + "%d" % leading)

    p.show_xy("John Q. Doe", left, y)
    p.continue_text("255 Customer Lane")
    p.continue_text("Suite B")
    p.continue_text("12345 User Town")
    p.continue_text("Everland")

    # Print the header and date

    p.setfont(boldfont, fontsize)
    y = 300
    p.show_xy("INVOICE",   left, y)

    buf = time.strftime("%x", time.gmtime(time.time()))
    p.fit_textline(buf, right, y, "position {100 0}")

    # Print the invoice header line
    p.setfont(boldfont, fontsize)

    # "position {0 0}" is left-aligned, "position {100 0}" right-aligned
    y = 370
    buf = "\tITEM\tDESCRIPTION\tQUANTITY\tPRICE\tAMOUNT"
    optlist = baseopt + " font " + repr(boldfont)

    textflow = p.create_textflow(buf, optlist);

    if textflow == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.fit_textflow(textflow, left, y-leading, right, y, "");
    p.delete_textflow(textflow);

    # Print the article list

    y += 2*leading
    total = 0

    optlist = baseopt + " font " + repr(regularfont)

    for i in range(0, ARTICLECOUNT, 1):
        sum = data_price[i] * data_quantity[i]

        buf = "\t" + repr(i+1) + "\t" + data_name[i] + "\t" + \
            repr(data_quantity[i]) + "\t" + "%.2f" % data_price[i] + \
            "\t" + "%.2f" % sum

        textflow = p.create_textflow(buf, optlist)

        if textflow == -1:
            raise PDFlibException("Error: " + p.get_errmsg())

        p.fit_textflow(textflow, left, y-leading, right, y, "")
        p.delete_textflow(textflow)

        y += leading;
        total += sum;


    y += leading

    p.setfont(boldfont, fontsize)
    buf =  "%.2f" % total
    p.fit_textline(buf, right, y, "position {100 0}")

    # Print the closing text

    y += 5*leading

    optlist = "alignment=justify leading=120% " + \
     "fontname=Helvetica fontsize=12 encoding=host "

    textflow = p.create_textflow(closingtext, optlist)

    if textflow == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.fit_textflow(textflow, left, y + 6*leading, right, y, "")
    p.delete_textflow(textflow)

    p.end_page_ext("")
    p.end_document("")
    p.close_pdi_document(stationery)

except PDFlibException:
    print("PDFlib exception occurred:\n[%d] %s: %s" %
	((p.get_errnum()), p.get_apiname(),  p.get_errmsg()))
    print_tb(exc_info()[2])

except Exception:
    print("Exception occurred: %s" % (exc_info()[0]))
    print_tb(exc_info()[2])

finally:
    p.delete()
