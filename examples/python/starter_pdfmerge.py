#!/usr/bin/python
# $Id: starter_pdfmerge.py,v 1.10 2012/09/13 14:26:21 rp Exp $
#
# PDF merge starter:
# Merge pages from multiple PDF documents; interactive elements (e.g. 
# bookmarks) will be dropped.
#
# required software: PDFlib+PDI/PPS 9
# required data: PDF documents

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

def printf(format, *args):
    sys.stdout.write(format % args)

# This is where the data files are. Adjust as necessary.
searchpath = "F:\\PDFlib\\examples\\data"
outfilename = "starter_pdfmerge.pdf"

pdffiles = (
        "PDFlib-real-world.pdf",
        "PDFlib-datasheet.pdf",
        "TET-datasheet.pdf",
        "PLOP-datasheet.pdf",
        "pCOS-datasheet.pdf"
)

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    if (p.begin_document(outfilename, "") == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_pdfmerge")

    for pdffile in (pdffiles):
        # Open the input PDF
        indoc = p.open_pdi_document(pdffile, "")
        if (indoc == -1):
            printf("Error: %s\n", p.get_errmsg())
            next

        endpage = p.pcos_get_number(indoc, "length:pages")

        # Loop over all pages of the input document
        for pageno in range(1, int(endpage)+1, 1):
            page = p.open_pdi_page(indoc, pageno, "")
            if (page == -1):
                printf("Error: %s\n", p.get_errmsg())
                next

            # Dummy page size; will be adjusted later
            p.begin_page_ext(10, 10, "")

            # Create a bookmark with the file name
            if (pageno == 1):
                p.create_bookmark(pdffile, "")

            # Place the imported page on the output page, and
            # adjust the page size
            
            p.fit_pdi_page(page, 0, 0, "adjustpage")
            p.close_pdi_page(page)

            p.end_page_ext("")

        p.close_pdi_document(indoc)

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
