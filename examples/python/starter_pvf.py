#!/usr/bin/python
# Id: starter_pvf.pl,v 1.1.2.2 2007/12/21 14:04:32 rjs Exp 
# PDFlib Virtual File system (PVF):
# Create a PVF file which holds an image or PDF, and import the data from the
# PVF file
#
# This avoids disk access and is especially useful when the same image or PDF
# is imported multiply. For examples, images which sit in a database don't
# have to be written and re-read from disk, but can be passed to PDFlib
# directly in memory. A similar technique can be used for loading other data
# such as fonts, ICC profiles, etc.
#
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: image file

# This is where the data files are. Adjust as necessary.
searchpath = "../data"
outfile = "starter_pvf.pdf"

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# create a new PDFlib object
p = PDFlib()

try:
    p.set_option("SearchPath={{" + searchpath +"}}")

    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    # Set an output path according to the name of the topic
    if p.begin_document(outfile, "") == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib Cookbook")
    p.set_info("Title", "PDFlib Virtual File System")

    # We just read some image data from a file; to really benefit
    # from using PVF read the data from a Web site or a database instead
    f = open("../data/PDFlib-logo.tif", "rb")
    f.seek(0, 2)
    filelen = f.tell()
    f.seek(0, 0)
    imagedata = f.read(filelen)


    p.create_pvf("/pvf/image", imagedata, "")

    # Load the image from the PVF
    image = p.load_image("auto", "/pvf/image", "")
    if image == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    # Fit the image on page 1
    p.begin_page_ext(595, 842, "")

    p.fit_image(image, 350, 750, "")

    p.end_page_ext("")

    # Fit the image on page 2
    p.begin_page_ext(595, 842, "")

    p.fit_image(image, 350, 50, "")

    p.end_page_ext("")

    # Delete the virtual file to free the allocated memory
    p.delete_pvf("/pvf/image")

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
