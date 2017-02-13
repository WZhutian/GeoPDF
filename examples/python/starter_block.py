#!/usr/bin/python
# Id: starter_block.php,v 1.11.2.3 2016/07/22 14:06:26 rp Exp 
#
# Block starter:
# Import a PDF page containing blocks and fill text and image
# blocks with some data. For each addressee of the simulated
# mailing a separate page with personalized information is
# generated.
# A real-world application would fill the Blocks with data from
# some external data source. We simulate this with static data.
#
# Required software: PPS 9
# Required data: input PDF, image

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

def printf(format, *args):
    sys.stdout.write(format % args)
    
# This is where the data files are. Adjust as necessary.
searchpath = "../data"
outfile = "starter_block.pdf"
infile = "block_template.pdf"
imagefile = "new.jpg"

# Names of the recipient-specific Blocks contained on the imported page
addressblocks = [
    "name", "street", "city"
]

# number of address blocks
nblocks = len(addressblocks)

# Personalization data for the recipients
recipients = [
    ["Mr Maurizio Moroni", "Strada Provinciale 124", "Reggio Emilia"],
    ["Ms Dominique Perrier", "25, rue Lauriston", "Paris"],
    ["Mr Liu Wong", "55 Grizzly Peak Rd.", "Butte"]
]

nrecipients = len(recipients)

# Static text simulates database-driven main contents
blockdata = [
  ["intro", "Dear Paper Planes Fan,"],
  ["announcement",
    "Our <fillcolor=red>BEST PRICE OFFER<fillcolor=black> includes today:" +
    "\n\n" +
    "Long Distance Glider\nWith this paper rocket you can s all your " +
    "messages even when sitting in a hall or in the cinema pretty near " +
    "the back.\n\n" +
    "Giant Wing\nAn unbelievable sailplane! It is amazingly robust and " +
    "can even do aerobatics. But it is best suited to gliding.\n\n" +
    "Cone Head Rocket\nThis paper arrow can be thrown with big swing. " +
    "We launched it from the roof of a hotel. It stayed in the air a " +
    "long time and covered a considerable distance.\n\n" +
    "Super Dart\nThe super dart can fly giant loops with a radius of 4 " +
    "or 5 meters and cover very long distances. Its heavy cone point is " +
    "slightly bowed upwards to get the lift required for loops.\n\n" +
    "Visit us on our Web site at www.kraxi.com!"],
  ["goodbye", "Yours sincerely,\nVictor Kraxi"]
]

# create a new PDFlib object
p = PDFlib()

try:
    p.set_option("SearchPath={{" + searchpath +"}}")

    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    if (p.begin_document(outfile,
            "destination={type=fitwindow} pagelayout=singlepage") == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_block")

 # Open the Block template which contains PDFlib Blocks
    indoc = p.open_pdi_document(infile, "")
    if (indoc == -1): 
      raise PDFlibException("Error: " + p.get_errmsg())
    
    no_of_input_pages = p.pcos_get_number(indoc, "length:pages")
    # Prepare all pages of the input document. We assume a small
    # number of input pages and a large number of generated output
    # pages. Therefore it makes sense to keep the input pages
    # open instead of opening the pages again for each recipient.
    
    pagehandles = {}
    for pageno in xrange(1, int(no_of_input_pages)+1):
      # Open the first page and clone the page size
      pagehandles[pageno] = p.open_pdi_page(indoc, pageno, "cloneboxes")
      if (pagehandles[pageno] == -1): 
        raise PDFlibException("Error: " + p.get_errmsg())
      
    

    image = p.load_image("auto", imagefile, "")

    if (image == -1): 
      raise PDFlibException("Error: " + p.get_errmsg())
    
    # Duplicate input pages for each recipient and fill Blocks

    for i in xrange (0, nrecipients):
    
      # Loop over all pages of the input document
      for pageno in xrange(1, int(no_of_input_pages)+1):
      # Start the next output page. The dummy size will be
        # replaced with the cloned size of the input page.
         
        p.begin_page_ext(10, 10, "")

        # Place the imported page on the output page, and clone all
        # page boxes which are present in the input page this will
        # override the dummy size used in begin_page_ext().
        
        p.fit_pdi_page(pagehandles[pageno], 0, 0, "cloneboxes")

        # Option list for text blocks
        optlist = "encoding=unicode embedding"

        # Loop over all recipient-specific Blocks. Fill each
        # Block with the corresponding person's address data.
        
        for j in xrange(0, nblocks):
        
          # Check whether the Block is present on the imported page
          # type "dictionary" means that the Block is present.
            
          objtype = p.pcos_get_string(indoc, 
              "type:pages[" + repr(pageno-1) + "]/blocks/" + addressblocks[j])
          if (objtype == "dict"):
            if (p.fill_textblock(pagehandles[pageno], addressblocks[j],
              recipients[i][j], optlist) == -1):
              printf("Warning: %s\n", p.get_errmsg())
        
        # Loop over the remaining text Blocks. These are filled with 
        # the same data for each recipient. 
        for j in xrange (0, len(blockdata)):
          # Check whether the Block is present on the page
          objtype = p.pcos_get_string(indoc, 
                "type:pages[" + repr(pageno-1) + "]/blocks/" + blockdata[j][0])
                
          if (objtype == "dict"):
            if (p.fill_textblock(pagehandles[pageno], blockdata[j][0],
              blockdata[j][1], optlist) == -1):
                printf("Warning: %s\n", p.get_errmsg())
        
        # Fill the icon Block if it is present on the imported page
        objtype = p.pcos_get_string(indoc, 
                "type:pages[" + repr(pageno-1) + "]/blocks/icon")
                
        if (objtype == "dict"):
          if (p.fill_imageblock(pagehandles[pageno], "icon", image, "") == -1):
              printf("Warning: %s\n", p.get_errmsg())

        p.end_page_ext("")
      
    

    # Close all input pages
    for pageno in xrange (1, int(no_of_input_pages)+1):
      p.close_pdi_page(pagehandles[pageno])
    
    p.close_pdi_document(indoc)
    p.close_image(image)

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
