#!/usr/bin/python
# $Id: businesscard.py,v 1.18 2012/09/13 14:26:21 rp Exp $
#
# PDFlib client: block processing example in Python
#

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

infile = "boilerplate.pdf"

# This is where font/image/PDF input files live. Adjust as necessary.
#
# Note that this directory must also contain the LuciduxSans font outline
# and metrics files.
#
searchpath = "F:\\PDFlib\\examples\\data"

data_name = [
 "name",
 "business.title",
 "business.address.line1",
 "business.address.city",
 "business.telephone.voice",
 "business.telephone.fax",
 "business.email",
 "business.homepage" ]

data_value = [
 "Victor Kraxi",
 "Chief Paper Officer",
 "17, Aviation Road",
 "Paperfield",
 "phone +1 234 567-89",
 "fax +1 234 567-98",
 "victor@kraxi.com",
 "www.kraxi.com" ]

BLOCKCOUNT = 8

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    # Set the search path for fonts and PDF files
    p.set_option("SearchPath={{" + searchpath +"}}")

    if p.begin_document("businesscard.pdf", "") == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "businesscard.py")
    p.set_info("Author", "Thomas Merz")
    p.set_info("Title","PDFlib block processing sample (C)")

    blockcontainer = p.open_pdi_document(infile, "")
    if blockcontainer == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    page = p.open_pdi_page(blockcontainer, 1, "")
    if page == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.begin_page_ext(20, 20, "")           # dummy page size

    # This will adjust the page size to the block container's size.
    p.fit_pdi_page(page, 0, 0, "adjustpage")

    # Fill all text blocks with dynamic data
    for i in range(0, BLOCKCOUNT, 1):
        if p.fill_textblock(page, data_name[i], data_value[i], \
                    "embedding encoding=unicode") == -1:
            print("Warning: " + p.get_errmsg() + "\n")

    p.end_page_ext("")
    p.close_pdi_page(page)

    p.end_document("")
    p.close_pdi_document(blockcontainer)

except PDFlibException:
    print("PDFlib exception occurred:\n[%d] %s: %s" %
	((p.get_errnum()), p.get_apiname(),  p.get_errmsg()))
    print_tb(exc_info()[2])

except Exception:
    print("Exception occurred: %s" % (exc_info()[0]))
    print_tb(exc_info()[2])

finally:
    p.delete()
