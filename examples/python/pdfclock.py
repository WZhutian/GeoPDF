#!/usr/bin/python
# $Id: pdfclock.py,v 1.19 2011/11/23 17:19:37 rjs Exp $
#
# PDFlib client: pdfclock example in Python
#

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *
from time import *

RADIUS = 200.0
MARGIN = 20.0

p = PDFlib()

try:
    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    if p.begin_document("pdfclock.pdf", "") == -1:
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "pdfclock.py")
    p.set_info("Author", "Thomas Merz")
    p.set_info("Title", "PDF clock (Python)")

    p.begin_page(2 * (RADIUS + MARGIN), 2 * (RADIUS + MARGIN))

    p.translate(RADIUS + MARGIN, RADIUS + MARGIN)
    p.setcolor("fillstroke", "rgb", 0.0, 0.0, 1.0, 0.0)
    p.save()

    # minute strokes 
    p.setlinewidth(2.0)
    for alpha in range(0, 360, 6):
        p.rotate(6.0)
        p.moveto(RADIUS, 0.0)
        p.lineto(RADIUS-MARGIN/3, 0.0)
        p.stroke()

    p.restore()
    p.save()

    # 5 minute strokes
    p.setlinewidth(3.0)
    for alpha in range(0, 360, 30):
        p.rotate(30.0)
        p.moveto(RADIUS, 0.0)
        p.lineto(RADIUS-MARGIN, 0.0)
        p.stroke()

    (tm_year, tm_month, tm_day,
    tm_hour, tm_min, tm_sec, 
    tm_weekday, tm_julian, tm_ds) = localtime(time())

    # draw hour hand 
    p.save()
    p.rotate((-((tm_min/60.0) + tm_hour - 3.0) * 30.0))
    p.moveto(-RADIUS/10, -RADIUS/20)
    p.lineto(RADIUS/2, 0.0)
    p.lineto(-RADIUS/10, RADIUS/20)
    p.closepath()
    p.fill()
    p.restore()

    # draw minute hand
    p.save()
    p.rotate((-((tm_sec/60.0) + tm_min - 15.0) * 6.0))
    p.moveto(-RADIUS/10, -RADIUS/20)
    p.lineto(RADIUS * 0.8, 0.0)
    p.lineto(-RADIUS/10, RADIUS/20)
    p.closepath()
    p.fill()
    p.restore()

    # draw second hand
    p.setcolor("fillstroke", "rgb", 1.0, 0.0, 0.0, 0.0)
    p.setlinewidth(2)
    p.save()
    p.rotate(-((tm_sec - 15.0) * 6.0))
    p.moveto(-RADIUS/5, 0.0)
    p.lineto(RADIUS, 0.0)
    p.stroke()
    p.restore()

    # draw little circle at center
    p.circle(0, 0, RADIUS/30)
    p.fill()

    p.restore()

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
