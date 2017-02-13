#!/usr/bin/python
# $Id: starter_webform.py,v 1.14.2.3 2014/05/08 12:59:46 rp Exp $
#
# Webform starter:
# create a linearized PDF (for fast delivery over the Web, also known
# as "fast Web view") which is encrypted and contains some form fields.
# A few lines of JavaScript are inserted as "page open" action to
# automatically populate the date field with the current date.
#
# required software: PDFlib/PDFlib+PDI/PPS 9
# required data: font file

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary. 
searchpath = "../data";

outfilename = "starter_webform.pdf"

llx=150; lly=550; urx=350; ury=575

# JavaScript for automatically filling the date into a form field
js = "var d = util.printd(\"mm/dd/yyyy\", new Date());" \
    "var date = this.getField(\"date\");" \
    "date.value = d;"

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return searchpath={{" + searchpath +"}}")

    # Prevent changes with a master password
    optlist = "linearize masterpassword=pdflib permissions={nomodify}"

    if (p.begin_document(outfilename, optlist) == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_webform")

    optlist = "script[" + repr(len(js)) + "]={" + js + "}"
    action = p.create_action("JavaScript", optlist)

    optlist = "action={open=" + repr(action) + "}"
    p.begin_page_ext(595, 842, optlist)

    font = p.load_font("LinLibertine_R", "winansi", "")
    if font == -1:
        raise PDFlibException("Error: " + p.get_errmsg() + "\n")

    p.setfont(font, 24)

    p.fit_textline("Date: ", 125, lly+5, "position={right bottom}")

    # The tooltip will be used as rollover text for the field
    optlist = \
        "tooltip={Date (will be filled automatically)} " \
        "bordercolor={gray 0} font=" + repr(font)
    p.create_field(llx, lly, urx, ury, "date", "textfield", optlist)

    lly-=100; ury-=100
    p.fit_textline("Name: ", 125, lly+5, "position={right bottom}")

    optlist = "tooltip={Enter your name here} bordercolor={gray 0} font=" + repr(font)
    p.create_field(llx, lly, urx, ury, "name", "textfield", optlist)

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
