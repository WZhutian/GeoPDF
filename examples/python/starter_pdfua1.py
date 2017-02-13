#!/usr/bin/python
# Id: starter_pdfua1.pl,v 1.1 2013/01/16 14:35:01 rp Exp $
# PDF/UA-1 starter:
# Create PDF/UA-1 document with various content types including structure
# elements, artifacts, and interactive elements.
# 
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: font file, image
# 

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *


# This is where the data files are. Adjust as necessary. 
searchpath = "../data"
imagefile = "lionel.jpg"
p = PDFlib()

try:

    # errorpolicy=exception means that the program will stop
    # if one of the API function runs into a problem.
    # 
    p.set_option("errorpolicy=exception searchPath={{" + searchpath + "}}")

    p.begin_document("starter_pdfua1.pdf",
	"pdfua=PDF/UA-1 lang=en " +\
	"tag={tagname=Document Title={PDFlib PDF/UA-1 demo}}") 

    p.set_info("Creator", "starter_pdfua1.py")
    p.set_info("Title", "PDFlib PDF/UA-1 demo")

    # Automatically create spaces between chunks of text 
    p.set_option("autospace=true")

    p.begin_page_ext(0, 0,
	    "width=a4.width height=a4.height taborder=structure")

    p.create_bookmark("PDF/UA-1 demo", "")

    font = p.load_font("LinLibertine_R", "unicode", "embedding")

    p.setfont(font, 24.0)

    # =================== Simple text  ======================== 

    # Use abbreviated tagging with the "tag" option 
    p.fit_textline("Introduction to Paper Planes",
	50, 700, "tag={tagname=H1 Title={Introduction}} fontsize=24")

    p.fit_textline(
	"Paper planes can be made from any kind of paper.", 
	50, 675, "tag={tagname=P} fontsize=12")

    p.fit_textline("Most paper planes don't have an engine.", 
	50, 650, "tag={tagname=P} fontsize=12")

    # =================== Interactive Link ======================== 
    id_p = p.begin_item("P", "")
    id_link = p.begin_item("Link", "Title={Kraxi on the Web}")

    # Create visible content which represents the link 
    p.fit_textline("Learn more on the Kraxi website.", 
	50, 625,
	"matchbox={name={kraxi.com}} fontsize=12 " +\
	"strokecolor=blue fillcolor=blue underline")

    # Create URI action 
    action = p.create_action("URI", "url={http://www.kraxi.com}")

    # Create Link annotation on named matchbox "kraxi.com".
    # This automatically creates an OBJR (object reference) element.

    optlist = "linewidth=0 usematchbox={kraxi.com} " +\
	"contents={Link to Kraxi Inc. Web site} " +\
	"action={activate=" + repr(action) + " } "
    p.create_annotation(0, 0, 0, 0, "Link", optlist)

    p.end_item(id_link)
    p.end_item(id_p)

    # =================== Image  ======================== 
    id_p = p.begin_item("P", "")
    image = p.load_image("auto", imagefile, "")

    p.fit_image(image, 50, 400,
	"tag={tagname=Figure Alt={Image of Kraxi waiting for customers.}} " +\
	"scale=0.5")
    p.close_image(image)
    p.end_item(id_p)

    # =================== Artifact  ======================== 
    p.fit_textline("Page 1", 250, 100,
	"tag={tagname=Artifact} fontsize=12")

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

