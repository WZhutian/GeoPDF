# $Id: starter_opentype.py,v 1.3.2.1 2013/07/05 11:26:46 rp Exp $
# Starter sample for OpenType font features
#
# Demonstrate various typographic OpenType features after checking
# whether a particular feature is supported in a font.
#
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: suitable fonts with OpenType feature tables
#
# This sample uses a default font which includes a few features.
# For better results you should replace the default font with a suitable
# commercial font. Depending on the implementation of the features you
# may also have to replace the sample text below.
#
# Some ideas for suitable test fonts:
# Palatino Linotype: standard Windows font with many OpenType features

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "F:\\PDFlib\\examples\\data"
outfile = "starter_opentype.pdf"

llx = 50
lly = 50
urx = 800
ury = 550

# This font will be used unless another one is specified in the table
defaulttestfont = "LinLibertine_R"

headers = [
        "OpenType feature",
        "Option list",
        "Font name",
        "Raw input (feature disabled)",
        "Feature enabled"
]
    
# expects an array with 4 elements and returns a corresponding dictionary with
# the keys "description", "fontname", "feature", "text"
def make_testcase_dict(x):
  assert len(x) == 4
  return dict(zip(["description", "fontname", "feature", "text"], x))

testcases = map(
    make_testcase_dict,
    [
        [
          "ligatures",
          "",
          "liga",
          "ff fi fl ffi ffl"
        ],
        [
          "discretionary ligatures",
          "",
          "dlig",
          "ch tz"
        ],
        [
          "historical ligatures",
          "",
          "hlig",
          "ct st"
        ],
        [
          "small capitals",
          "",
          "smcp",
          "PostScript"
        ],
        [
          "ordinals",
          "",
          "ordn",
          "1o 2a 3o"
        ],
        [
          "fractions",
          "",
          "frac",
          "1/2 1/4 3/4"
        ],
        [
          "alternate fractions",
          "",
          "afrc",
          "1/2 1/4 3/4"
        ],
        [
          "slashed zero",
          "",
          "zero",
          "0"
        ],
        [
          "historical forms",
          "",
          "hist",
          "s"
        ],
        [
          "proportional figures",
          "",
          "pnum",
          "0123456789"
        ],
        [
          "old-style figures",
          "",
          "onum",
          "0123456789"
        ],
        [
          "lining figures",
          "",
          "lnum",
          "0123456789"
        ],
        [
          "superscript",
          "",
          "sups",
          "0123456789"
        ],
        [
          "scientific inferiors",
          "",
          "sinf",
          "H2SO4"

        ]
    ]
)

p = PDFlib()

try:
    p.set_option("SearchPath={{" + searchpath +"}}")
    p.set_option("charref=true")

    # This means that formatting and other errors will raise an
    # exception. This simplifies our sample code, but is not
    # recommended for production code.
    p.set_option("errorpolicy=exception")

    # Set an output path according to the name of the topic
    if (p.begin_document(outfile, "") == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_opentype")

    # Start Page
    p.begin_page_ext(0, 0, "width=a4.height height=a4.width")

    table = -1
    row = 1
    
    # Table header
    col = 1
    for header in headers:
        optlist = (
           "fittextline={fontname=Helvetica-Bold encoding=unicode fontsize=12} "
           "margin=4"
        )
        table = p.add_table_cell(table, col, row, header, optlist)
        col += 1

    row += 1
    
    # Create a table with feature samples, one feature per table row
    for testcase in testcases:
        # Use the entry in the test table if available, and the
        # default test font otherwise. This way we can easily check
        # a font for all features, as well as insert suitable fonts
        # for individual features.
        if (len(testcase["fontname"]) > 0):
            testfont = testcase["fontname"]
        else:
            testfont = defaulttestfont

        col=1

        # Common option list for columns 1-3
        optlist = (
            "fittextline={fontname=Helvetica encoding=unicode fontsize=12} "
            "margin=4"
        )

        # Column 1: feature description
        table = p.add_table_cell(table, col, row, testcase["description"], optlist)

        col += 1
        
        # Column 2: option list
        buf = "features={%s}" % testcase["feature"]
        table = p.add_table_cell(table, col, row, buf, optlist)

        col += 1
        
        # Column 3: font name
        table = p.add_table_cell(table, col, row, testfont, optlist)

        col += 1
        
        # Column 4: raw input text with  feature disabled
        optlist = (
            "fittextline={fontname={%s} encoding=unicode fontsize=12 "
            "embedding} margin=4" % testfont
        )
        table = p.add_table_cell(table, col, row, testcase["text"], optlist)

        col += 1
        
        # Column 5: text with enabled feature, or warning if the
        # feature is not available in the font
        font = p.load_font(testfont, "unicode", "embedding")

        # Check whether font contains the required feature table
        optlist = "name=%s" % testcase["feature"]
        if (p.info_font(font, "feature", optlist) == 1):
            # feature is available: apply it to the text
            optlist = (
                 "fittextline={fontname={%s} encoding=unicode fontsize=12 "
                 "embedding features={%s}} margin=4" %
                 (testfont, testcase["feature"])
            )
            table = p.add_table_cell(table, col, row, testcase["text"], optlist)
        else:
            # feature is not available: emit a warning
            optlist = (
                "fittextline={fontname=Helvetica encoding=unicode "
                "fontsize=12 fillcolor=red} margin=4"
            )
            table = p.add_table_cell(table, col, row,
                    "(feature not available in this font)", optlist)
        
        row += 1

    # Place the table
    optlist = "header=1 fill={{area=rowodd fillcolor={gray 0.9}}} stroke={{line=other}}"
    result = p.fit_table(table, llx, lly, urx, ury, optlist)

    if (result == "_error"):
        raise PDFlibException("Couldn't place table: " + p.get_errmsg())

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
