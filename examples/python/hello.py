#!/usr/bin/python
# $Id: hello.py,v 1.22 2011/11/23 17:19:37 rjs Exp $
#
# PDFlib client: hello example in Python
#

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# create a new PDFlib object
p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    if p.begin_document("hello.pdf", "") == -1:
        raise Exception("Error: " + p.get_errmsg())

    p.set_info("Author", "Thomas Merz")
    p.set_info("Creator", "hello.py")
    p.set_info("Title", "Hello world (Python)")

    p.begin_page_ext(595, 842, "")

    font = p.load_font("Helvetica-Bold", "unicode", "")
    if font == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.setfont(font, 24)
    p.set_text_pos(50, 700)
    p.show("Hello world!")
    p.continue_text("(says Python)")
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
