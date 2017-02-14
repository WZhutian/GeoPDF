#!/usr/bin/python
# Id: starter_type3font.pl,v 1.1.2.3 2007/12/21 14:04:32 rjs Exp 
# Type 3 font starter:
# Create a simple Type 3 font from vector data
#
# Define a type 3 font with the glyphs "l" and "space" and output text with
# that font. In addition the glyph ".notdef" is defined which any undefined
# character will be mapped to.
#
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: none

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# create a new PDFlib object
p = PDFlib()

# This is where the data files are. Adjust as necessary.
searchpath = "F:\\PDFlib\\examples\\data"
outfile = "starter_type3font.pdf"

try:

    p.set_option("SearchPath={{" + searchpath +"}}")

    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    if p.begin_document(outfile, "") == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib Cookbook")
    p.set_info("Title", "Starter Type 3 Font")

    # Create the font "SimpleFont" containing the glyph "l",
    # the glyph "space" for spaces and the glyph ".notdef" for any
    # undefined character

    p.begin_font("SimpleFont",
                0.001, 0.0, 0.0, 0.001, 0.0, 0.0, "")
    # glyph for .notdef */
    p.begin_glyph_ext(0x0000, "width=266 boundingbox={0 0 0 0}")
    p.end_glyph()

    # glyph for U+0020 space */
    p.begin_glyph_ext(0x0020, "width=266 boundingbox={0 0 0 0}")
    p.end_glyph()

    # glyph for U+006C "l" */
    p.begin_glyph_ext(0x006C, "width=266 boundingbox={0 0 266 570}")
    p.setlinewidth(20)
    x = 197
    y = 10
    p.moveto(x, y)
    y += 530
    p.lineto(x, y)
    x -= 64
    p.lineto(x, y)
    y -= 530
    p.moveto(x, y)
    x += 128
    p.lineto(x, y)

    p.stroke()
    p.end_glyph()

    p.end_font()

    # Start page
    p.begin_page_ext(0, 0, "width=300 height=200")

    # Load the new "SimpleFont" font
    font = p.load_font("SimpleFont", "winansi", "")

    if font == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    # Output the characters "l" and "space" of the "SimpleFont" font.
    # The character "x" is undefined and will be mapped to ".notdef"

    buf = " font=" + repr(font) + " fontsize=40"
    p.fit_textline("lll lllxlll", 100, 100, buf)

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
