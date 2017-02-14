# $Id: starter_pdfx4.py,v 1.6 2012/09/13 14:26:21 rp Exp $
#
# PDF/X-4 starter:
# Create PDF/X-4 conforming output with layers and transparency
#
# The document contains transparent text which is allowed in
# PDF/X-4, but not earlier PDF/X standards.
#
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: font file, image file, ICC output intent profile
#                (see www.pdflib.com for ICC profiles)

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "F:\\PDFlib\\examples\\data"
imagefile = "zebra.tif"

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    if (p.begin_document("starter_pdfx4.pdf", "pdfx=PDF/X-4") == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_pdfx4")

    if (p.load_iccprofile("ISOcoated.icc", "usage=outputintent") == -1):
        print ("Please install the ICC profile package from "
               "www.pdflib.com to run the PDF/X-4 starter sample.\n")
        raise PDFlibException("Error: " + p.get_errmsg())

    # Define the layers; "defaultstate" specifies whether or not
    # the layer is visible when the page is opened.

    layer_english = p.define_layer("English text", "defaultstate=true")
    layer_german  = p.define_layer("German text", "defaultstate=false")
    layer_french  = p.define_layer("French text", "defaultstate=false")

    # Define a radio button relationship for the language layers.
    #
    optlist = ("group={%d %d %d}" %
	    (layer_english, layer_german, layer_french))
    p.set_layer_dependency("Radiobtn", optlist);

    layer_image = p.define_layer("Images", "defaultstate=true")
    
    p.begin_page_ext(595, 842, "")

    # Font embedding is required for PDF/X
    font = p.load_font("LuciduxSans-Oblique", "winansi", "embedding")

    if (font == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.setfont(font, 24)

    p.begin_layer(layer_english)

    p.fit_textline("PDF/X-4 starter sample with layers", 50, 700, "")

    p.begin_layer(layer_german)
    p.fit_textline("PDF/X-4 Starter-Beispiel mit Ebenen", 50, 700, "")

    p.begin_layer(layer_french)
    p.fit_textline("PDF/X-4 Starter exemple avec des calques", 50, 700, "")

    p.begin_layer(layer_image)

    p.setfont(font, 48)

    # The RGB image needs an ICC profile; we use sRGB.
    icc = p.load_iccprofile("sRGB", "")
    optlist = "iccprofile=%d" % icc
    image = p.load_image("auto", imagefile, optlist)

    if (image == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    # Place a diagonal stamp across the image area
    width = p.info_image(image, "width", "")
    height = p.info_image(image, "height", "")

    optlist = "boxsize={%f %f} stamp=ll2ur" % (width, height)
    p.fit_textline("Zebra", 0, 0, optlist)

    # Set transparency in the graphics state
    gstate = p.create_gstate("opacityfill=0.5")
    p.set_gstate(gstate)

    # Place the image on the page and close it
    p.fit_image(image, 0.0, 0.0, "")
    p.close_image(image)

    # Close all layers
    p.end_layer()

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
