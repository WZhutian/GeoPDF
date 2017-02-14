#!/usr/bin/python
# Id: starter_3d.pl,v 1.1.2.1 2008/02/20 22:06:41 rjs Exp $
# 3D Starter:
# Load a 3D model and create a 3D annotation from it.
#
# Define a 3D view and load some 3D data with the view defined. Then create
# an annotation containing the loaded 3D data with the defined 3D view as the
# initial view.
#
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: PRC data file
#

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# This is where the data files are. Adjust if necessary.
searchpath = "F:\\PDFlib\\examples\\data"
outfile = "starter_3d.pdf"

# create a new PDFlib object
p = PDFlib()

try:
    # Set errorpoliy to return, this means we must check return
    # values of begin_document() etc.
    # Set the search path for 3D data files

    p.set_option("errorpolicy=return SearchPath={{" + searchpath + "}}")


    # Start the document
    if p.begin_document(outfile, "compatibility=1.7ext3") == -1:
        raise Exception("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib Cookbook")
    p.set_info("Title", "starter_3d")

    p.begin_page_ext(0, 0, "width=a4.width height=a4.height")

    # Define a 3D view which shows the model from the top
    optlist = "type=PRC name=FirstView background={fillcolor=Lavender} " +\
		"camera2world={-1 0 0 0 1 0 0 0 -1 0.5 0 300}"
    view = p.create_3dview("First view", optlist)
    if view == -1:
        raise Exception("Error: " + p.get_errmsg())

    # Load some 3D data with the view defined above
    buf = "type=PRC views={" + repr(view) + "}"
    data = p.load_3ddata("riemann.prc", buf)
    if data == -1:
        raise Exception("Error: " + p.get_errmsg())

    # Create an annotation containing the loaded 3D data with the
    # defined 3D view as the initial view
    #
    buf = "name=annot usercoordinates contents=PRC 3Ddata=" + repr(data) \
        + " 3Dactivate={enable=open} 3Dinitialview=" + repr(view)
    p.create_annotation(116, 200, 447, 580, "3D", buf)

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
