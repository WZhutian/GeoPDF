#!/usr/bin/python
# $Id: starter_pcos.py,v 1.17 2013/03/13 10:57:13 rjs Exp $
#
# pCOS starter:
# Dump information from an existing PDF document
#
# required software: PDFlib+PDI/PPS 9
# required data: PDF input file

import sys
from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

def printf(format, *args):
    sys.stdout.write(format % args)

# This is where the data files are. Adjust as necessary.
searchpath = "F:\\PDFlib\\examples\\data"
pdfinput = "TET-datasheet.pdf"
docoptlist = "requiredmode=minimum"

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    # We do not create any output document, so no call to
    # begin_document() is required.


    # Open the input document
    doc = p.open_pdi_document(pdfinput, docoptlist)
    if (doc == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    # --------- general information (always available)

    pcosmode = p.pcos_get_number(doc, "pcosmode")

    printf("   File name: %s\n",
        p.pcos_get_string(doc, "filename"))

    printf(" PDF version: %s\n",
	p.pcos_get_string(doc, "pdfversionstring"))

    printf("  Encryption: %s\n",
        p.pcos_get_string(doc, "encrypt/description"))

    printf("   Master pw: %s\n",
        ((p.pcos_get_number(doc, "encrypt/master") != 0) and "yes" or "no"))

    printf("     User pw: %s\n",
        ((p.pcos_get_number(doc, "encrypt/user") != 0) and "yes" or "no"))

    printf("Text copying: %s\n",
        ((p.pcos_get_number(doc, "encrypt/nocopy") != 0) and "no" or "yes"))

    printf("  Linearized: %s\n\n",
        ((p.pcos_get_number(doc, "linearized") != 0) and "yes" or "no"))

    if (pcosmode == 0):
        printf("Minimum mode: no more information available\n\n")
        exit(0)

    # --------- more details (requires at least user password)
    printf("PDF/X status: %s\n", p.pcos_get_string(doc, "pdfx"))
        
    printf("PDF/A status: %s\n", p.pcos_get_string(doc, "pdfa"))
        
    xfa_present = p.pcos_get_string(doc,
                                 "type:/Root/AcroForm/XFA") != "null";
    printf("    XFA data: %s\n", xfa_present and "yes" or "no");
        
    printf("  Tagged PDF: %s\n",
        ((p.pcos_get_number(doc, "tagged") != 0) and "yes" or "no"))

    printf("No. of pages: %d\n",
        p.pcos_get_number(doc, "length:pages"))

    printf(" Page 1 size: width=%.3f, height=%.3f\n",
         p.pcos_get_number(doc, "pages[0]/width"),
         p.pcos_get_number(doc, "pages[0]/height"))

    count = p.pcos_get_number(doc, "length:fonts")
    printf("No. of fonts: %d\n",  count)

    for i in range (0, int(count), 1):
        fonts = "fonts[" + repr(i) + "]/embedded"
        if (p.pcos_get_number(doc, fonts) != 0):
            printf("embedded ")
        else:
            printf("unembedded ")

        fonts = "fonts[" + repr(i) + "]/type"
        printf(p.pcos_get_string(doc, fonts) + " font ")
        fonts = "fonts[" + repr(i) + "]/name"
        printf("%s\n", p.pcos_get_string(doc, fonts))

    printf("\n")

    plainmetadata = p.pcos_get_number(doc,
                                         "encrypt/plainmetadata") != 0
    if (pcosmode == 1 and not plainmetadata
                and p.pcos_get_number(doc, "encrypt/nocopy") != 0):
        print("Restricted mode: no more information available")
        exit(0)

    # ----- document Info keys and XMP metadata (requires master pw)

    count = p.pcos_get_number(doc, "length:/Info")

    for i in range (0, int(count), 1):
        info = "type:/Info[" + repr(i) + "]"
        objtype = p.pcos_get_string(doc, info)

        info = "/Info[" + repr(i) + "].key"
        key = p.pcos_get_string(doc, info)
        j = 12 - len(key)
        while (j > 0):
            printf(" ")
            j -= 1

        printf(key + ": ")

        # Info entries can be stored as string or name objects
        if (objtype == "name" or objtype == "string"):
            info = "/Info[" + repr(i) + "]"
            printf("'" + p.pcos_get_string(doc, info) + "'\n")
        else:
            info = "type:/Info[" + repr(i) + "]"
            printf("(" + p.pcos_get_string(doc, info) + " object)\n")

    printf("\nXMP metadata: ")


    objtype = p.pcos_get_string(doc, "type:/Root/Metadata")
    if (objtype == "stream"):
        contents = p.pcos_get_stream(doc, "", "/Root/Metadata")
        printf("%d bytes \n", len(contents))
        printf("")
    else:
        printf("not present\n")

    p.close_pdi_document(doc)

except PDFlibException:
    print("PDFlib exception occurred:\n[%d] %s: %s" %
	((p.get_errnum()), p.get_apiname(),  p.get_errmsg()))
    print_tb(exc_info()[2])

except Exception:
    print("Exception occurred: %s" % (exc_info()[0]))
    print_tb(exc_info()[2])

finally:
    p.delete()
