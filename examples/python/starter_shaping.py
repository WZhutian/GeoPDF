# $Id: starter_shaping.py,v 1.4 2012/09/13 14:26:21 rp Exp $
# Starter sample for text shaping features
# Demonstrate text shaping for Arabic, Hebrew, Devanagari, and Thai scripts
# Right-to-left text is reordered according to the Bidi algorithm.
#
# Required software: PDFlib/PDFlib+PDI/PPS 9
# Required data: suitable fonts for the scripts

from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "../data"
outfile = "starter_shaping.pdf"
llx = 50.0
lly = 50.0
urx = 800.0
ury = 550.0
headers = ["Language", "Raw input", "Reordered and shaped output"]

# expects an array with 5 elements and returns a corresponding dictionary with
# the keys "fontname", "optlist", "textflow", "language", "text"
def make_shaping_dict(x):
  assert len(x) == 5
  return dict(zip(["fontname", "optlist", "textflow", "language", "text"], x))

shapingsamples = map(
    make_shaping_dict,
    [
	# -------------------------- Arabic -------------------------- 
	[ "ScheherazadeRegOT", "shaping script=arab", 0, "Arabic",
	"&#x0627;&#x0644;&#x0639;&#x064E;&#x0631;&#x064E;&#x0628;&#x0650;"
	"&#x064A;&#x0629;" ],

	[ "ScheherazadeRegOT", "shaping script=arab", 0, "Arabic",
	"&#x0645;&#x0631;&#x062D;&#x0628;&#x0627;! (Hello)"
	],

	[ "ScheherazadeRegOT", "shaping script=arab", 0, "Arabic",
	"&#xFEFF;&#x0627;&#x0644;&#x0645;&#x0627;&#x062F;&#x0629;&#x0020;"
	"&#x0031;&#x0020;&#x064A;&#x0648;&#x0644;&#x062F;&#x0020;&#x062C;"
	"&#x0645;&#x064A;&#x0639;&#x0020;&#x0627;&#x0644;&#x0646;&#x0627;"
	"&#x0633;&#x0020;&#x0623;&#x062D;&#x0631;&#x0627;&#x0631;&#x064B;"
	"&#x0627;&#x0020;&#x0645;&#x062A;&#x0633;&#x0627;&#x0648;&#x064A;"
	"&#x0646;&#x0020;&#x0641;&#x064A;&#x0020;&#x0627;&#x0644;&#x0643;"
	"&#x0631;&#x0627;&#x0645;&#x0629;&#x0020;&#x0648;&#x0627;&#x0644;"
	"&#x062D;&#x0642;&#x0648;&#x0642;&#x002E;&#x0020;"
	],

	[ "ScheherazadeRegOT", "shaping script=arab", 0, "Arabic",
	"&#x0648;&#x0642;&#x062F;&#x0020;&#x0648;&#x0647;&#x0628;&#x0648;"
	"&#x0627;&#x0020;&#x0639;&#x0642;&#x0644;&#x0627;&#x064B;&#x0020;"
	"&#x0648;&#x0636;&#x0645;&#x064A;&#x0631;&#x064B;&#x0627;&#x0020;"
	"&#x0648;&#x0639;&#x0644;&#x064A;&#x0647;&#x0645;&#x0020;&#x0623;"
	"&#x0646;&#x0020;&#x064A;&#x0639;&#x0627;&#x0645;&#x0644;&#x0020;"
	"&#x0628;&#x0639;&#x0636;&#x0647;&#x0645;&#x0020;&#x0628;&#x0639;"
	"&#x0636;&#x064B;&#x0627;&#x0020;&#x0628;&#x0631;&#x0648;&#x062D;"
	"&#x0020;&#x0627;&#x0644;&#x0625;&#x062E;&#x0627;&#x0621;&#x002E;"
	],

	# -------------------------- Hebrew --------------------------
	[ "SILEOT", "shaping script=hebr", 0, "Hebrew",
	  "&#x05E2;&#x05B4;&#x05D1;&#x05B0;&#x05E8;&#x05B4;&#x05D9;&#x05EA;"
	],

	[ "SILEOT", "shaping script=hebr", 0, "Hebrew",
	"&#x05E1;&#x05E2;&#x05D9;&#x05E3;&#x0020;&#x05D0;&#x002E;&#x0020;"
	"&#x05DB;&#x05DC;&#x0020;&#x05D1;&#x05E0;&#x05D9;&#x0020;&#x05D0;"
	"&#x05D3;&#x05DD;&#x0020;&#x05E0;&#x05D5;&#x05DC;&#x05D3;&#x05D5;"
	"&#x0020;&#x05D1;&#x05E0;&#x05D9;&#x0020;&#x05D7;&#x05D5;&#x05E8;"
	"&#x05D9;&#x05DF;&#x0020;&#x05D5;&#x05E9;&#x05D5;&#x05D5;&#x05D9;"
	"&#x05DD;&#x0020;&#x05D1;&#x05E2;&#x05E8;&#x05DB;&#x05DD;&#x0020;"
	"&#x05D5;&#x05D1;&#x05D6;&#x05DB;&#x05D5;&#x05D9;&#x05D5;&#x05EA;"
	"&#x05D9;&#x05D4;&#x05DD;&#x002E;&#x0020;"
	],

	[ "SILEOT", "shaping script=hebr", 0, "Hebrew",
	"&#x05DB;&#x05D5;&#x05DC;&#x05DD;&#x0020;&#x05D7;&#x05D5;&#x05E0;"
	"&#x05E0;&#x05D5;&#x0020;&#x05D1;&#x05EA;&#x05D1;&#x05D5;&#x05E0;"
	"&#x05D4;&#x0020;&#x05D5;&#x05D1;&#x05DE;&#x05E6;&#x05E4;&#x05D5;"
	"&#x05DF;&#x002C;&#x0020;"
	],

	[ "SILEOT", "shaping script=hebr", 0, "Hebrew",
	"&#x05DC;&#x05E4;&#x05D9;&#x05DB;&#x05DA;&#x0020;&#x05D7;&#x05D5;"
	"&#x05D1;&#x05D4;&#x0020;&#x05E2;&#x05DC;&#x05D9;&#x05D4;&#x05DD;"
	"&#x0020;&#x05DC;&#x05E0;&#x05D4;&#x05D5;&#x05D2;&#x0020;&#x05D0;"
	"&#x05D9;&#x05E9;&#x0020;&#x05D1;&#x05E8;&#x05E2;&#x05D4;&#x05D5;"
	"&#x0020;&#x05D1;&#x05E8;&#x05D5;&#x05D7;&#x0020;&#x05E9;&#x05DC;"
	"&#x0020;&#x05D0;&#x05D7;&#x05D5;&#x05D4;&#x002E;"
	],

	# -------------------------- Hindi -------------------------- 
	[ "raghu8", "shaping script=deva", 1, "Hindi",
	  "&#x0939;&#x093F;&#x0928;&#x094D;&#x0926;&#x0940;"
	],

	[ "raghu8", "shaping script=deva advancedlinebreak", 1, "Hindi",
	"&#x0905;&#x0928;&#x0941;&#x091A;&#x094D;&#x091B;&#x0947;&#x0926;"
	"&#x0020;&#x0967;&#x002E;&#x0020;&#x0938;&#x092D;&#x0940;&#x0020;"
	"&#x092E;&#x0928;&#x0941;&#x0937;&#x094D;&#x092F;&#x094B;&#x0902;"
	"&#x0020;&#x0915;&#x094B;&#x0020;&#x0917;&#x094C;&#x0930;&#x0935;"
	"&#x0020;&#x0914;&#x0930;&#x0020;&#x0905;&#x0927;&#x093F;&#x0915;"
	"&#x093E;&#x0930;&#x094B;&#x0902;&#x0020;&#x0915;&#x0947;&#x0020;"
	"&#x092E;&#x093E;&#x092E;&#x0932;&#x0947;&#x0020;&#x092E;&#x0947;"
	"&#x0902;&#x0020;&#x091C;&#x0928;&#x094D;&#x092E;&#x091C;&#x093E;"
	"&#x0924;&#x0020;&#x0938;&#x094D;&#x0935;&#x0924;&#x0928;&#x094D;"
	"&#x0924;&#x094D;&#x0930;&#x0924;&#x093E;&#x0020;&#x0914;&#x0930;"
	"&#x0020;&#x0938;&#x092E;&#x093E;&#x0928;&#x0924;&#x093E;&#x0020;"
	"&#x092A;&#x094D;&#x0930;&#x093E;&#x092A;&#x094D;&#x0924;&#x0020;"
	"&#x0939;&#x0948;&#x0020;&#x0964;&#x0020;&#x0909;&#x0928;&#x094D;"
	"&#x0939;&#x0947;&#x0902;&#x0020;&#x092C;&#x0941;&#x0926;&#x094D;"
	"&#x0918;&#x093F;&#x0020;&#x0914;&#x0930;&#x0020;&#x0905;&#x0928;"
	"&#x094D;&#x0924;&#x0930;&#x093E;&#x0924;&#x094D;&#x092E;&#x093E;"
	"&#x0020;&#x0915;&#x0940;&#x0020;&#x0926;&#x0947;&#x0928;&#x0020;"
	"&#x092A;&#x094D;&#x0930;&#x093E;&#x092A;&#x094D;&#x0924;&#x0020;"
	"&#x0939;&#x0948;&#x0020;&#x0914;&#x0930;&#x0020;&#x092A;&#x0930;"
	"&#x0938;&#x094D;&#x092A;&#x0930;&#x0020;&#x0909;&#x0928;&#x094D;"
	"&#x0939;&#x0947;&#x0902;&#x0020;&#x092D;&#x093E;&#x0908;&#x091A;"
	"&#x093E;&#x0930;&#x0947;&#x0020;&#x0915;&#x0947;&#x0020;&#x092D;"
	"&#x093E;&#x0935;&#x0020;&#x0938;&#x0947;&#x0020;&#x092C;&#x0930;"
	"&#x094D;&#x0924;&#x093E;&#x0935;&#x0020;&#x0915;&#x0930;&#x0928;"
	"&#x093E;&#x0020;&#x091A;&#x093E;&#x0939;&#x093F;&#x090F;&#x0020;"
	"&#x0964;"
	],

	# -------------------------- Sanskrit --------------------------
	[ "raghu8", "shaping script=deva", 1, "Sanskrit",
	"&#x0938;&#x0902;&#x0938;&#x094D;&#x0915;&#x0943;&#x0924;&#x092E;"
	"&#x094D;"
	],

	[ "raghu8", "shaping script=deva", 1, "Sanskrit",
	"&#x0905;&#x0928;&#x0941;&#x091A;&#x094D;&#x091B;&#x0947;&#x0926;"
	"&#x003A;&#x0020;&#x0031;&#x0020;&#x0938;&#x0930;&#x094D;&#x0935;"
	"&#x0947;&#x0020;&#x092E;&#x093E;&#x0928;&#x0935;&#x093E;&#x003A;"
	"&#x0020;&#x0938;&#x094D;&#x0935;&#x0924;&#x0928;&#x094D;&#x0924;"
	"&#x094D;&#x0930;&#x093E;&#x003A;&#x0020;&#x0938;&#x092E;&#x0941;"
	"&#x0924;&#x094D;&#x092A;&#x0928;&#x094D;&#x0928;&#x093E;&#x003A;"
	"&#x0020;&#x0935;&#x0930;&#x094D;&#x0924;&#x0928;&#x094D;&#x0924;"
	"&#x0947;&#x0020;&#x0905;&#x092A;&#x093F;&#x0020;&#x091A;&#x002C;"
	"&#x0020;&#x0917;&#x094C;&#x0930;&#x0935;&#x0926;&#x0943;&#x0936;"
	"&#x093E;&#x0020;&#x0905;&#x0927;&#x093F;&#x0915;&#x093E;&#x0930;"
	"&#x0926;&#x0943;&#x0936;&#x093E;&#x0020;&#x091A;&#x0020;&#x0938;"
	"&#x092E;&#x093E;&#x0928;&#x093E;&#x003A;&#x0020;&#x090F;&#x0935;"
	"&#x0020;&#x0935;&#x0930;&#x094D;&#x0924;&#x0928;&#x094D;&#x0924;"
	"&#x0947;&#x0964;&#x0020;&#x090F;&#x0924;&#x0947;&#x0020;&#x0938;"
	"&#x0930;&#x094D;&#x0935;&#x0947;&#x0020;&#x091A;&#x0947;&#x0924;"
	"&#x0928;&#x093E;&#x002D;&#x0924;&#x0930;&#x094D;&#x0915;&#x002D;"
	"&#x0936;&#x0915;&#x094D;&#x0924;&#x093F;&#x092D;&#x094D;&#x092F;"
	"&#x093E;&#x0902;&#x0020;&#x0938;&#x0941;&#x0938;&#x092E;&#x094D;"
	"&#x092A;&#x0928;&#x094D;&#x0928;&#x093E;&#x003A;&#x0020;&#x0938;"
	"&#x0928;&#x094D;&#x0924;&#x093F;&#x0964;&#x0020;&#x0905;&#x092A;"
	"&#x093F;&#x0020;&#x091A;&#x002C;&#x0020;&#x0938;&#x0930;&#x094D;"
	"&#x0935;&#x0947;&#x093D;&#x092A;&#x093F;&#x0020;&#x092C;&#x0928;"
	"&#x094D;&#x0927;&#x0941;&#x0924;&#x094D;&#x0935;&#x002D;&#x092D;"
	"&#x093E;&#x0935;&#x0928;&#x092F;&#x093E;&#x0020;&#x092A;&#x0930;"
	"&#x0938;&#x094D;&#x092A;&#x0930;&#x0902;&#x0020;&#x0935;&#x094D;"
	"&#x092F;&#x0935;&#x0939;&#x0930;&#x0928;&#x094D;&#x0924;&#x0941;"
	"&#x0964;"
	],

	# -------------------------- Thai --------------------------
	[ "Norasi", "shaping script=thai advancedlinebreak locale=THA", 1, "Thai",
	  "&#x0E44;&#x0E17;&#x0E22;"
	],

	[ "Norasi", "shaping script=thai advancedlinebreak", 1, "Thai",
	"&#x0E02;&#x0E49;&#x0E2D;&#x0020;&#x0031;&#x0020;&#x0E21;&#x0E19;"
	"&#x0E38;&#x0E29;&#x0E22;&#x0E4C;&#x0E17;&#x0E31;&#x0E49;&#x0E07;"
	"&#x0E2B;&#x0E25;&#x0E32;&#x0E22;&#x0E40;&#x0E01;&#x0E34;&#x0E14;"
	"&#x0E21;&#x0E32;&#x0E21;&#x0E35;&#x0E2D;&#x0E34;&#x0E2A;&#x0E23;"
	"&#x0E30;&#x0E41;&#x0E25;&#x0E30;&#x0E40;&#x0E2A;&#x0E21;&#x0E2D;"
	"&#x0E20;&#x0E32;&#x0E04;&#x0E01;&#x0E31;&#x0E19;&#x0E43;&#x0E19;"
	"&#x0E40;&#x0E01;&#x0E35;&#x0E22;&#x0E23;&#x0E15;&#x0E34;&#x0E28;"
	"&#x0E31;&#x0E01;&#x0E14;&#x005B;&#x0E40;&#x0E01;&#x0E35;&#x0E22;"
	"&#x0E23;&#x0E15;&#x0E34;&#x0E28;&#x0E31;&#x0E01;&#x0E14;&#x0E34;"
	"&#x0E4C;&#x005D;&#x0E41;&#x0E25;&#x0E30;&#x0E2A;&#x0E34;&#x0E17;"
	"&#x0E18;&#x0E34;&#x0020;&#x0E15;&#x0E48;&#x0E32;&#x0E07;&#x0E21;"
	"&#x0E35;&#x0E40;&#x0E2B;&#x0E15;&#x0E38;&#x0E1C;&#x0E25;&#x0E41;"
	"&#x0E25;&#x0E30;&#x0E21;&#x0E42;&#x0E19;&#x0E18;&#x0E23;&#x0E23;"
	"&#x0E21;&#x0020;&#x0E41;&#x0E25;&#x0E30;&#x0E04;&#x0E27;&#x0E23;"
	"&#x0E1B;&#x0E0F;&#x0E34;&#x0E1A;&#x0E31;&#x0E15;&#x0E34;&#x0E15;"
	"&#x0E48;&#x0E2D;&#x0E01;&#x0E31;&#x0E19;&#x0E14;&#x0E49;&#x0E27;"
	"&#x0E22;&#x0E40;&#x0E08;&#x0E15;&#x0E19;&#x0E32;&#x0E23;&#x0E21;"
	"&#x0E13;&#x0E4C;&#x0E41;&#x0E2B;&#x0E48;&#x0E07;&#x0E20;&#x0E23;"
	"&#x0E32;&#x0E14;&#x0E23;&#x0E20;&#x0E32;&#x0E1E;"
	]
    ]
)

p = PDFlib()

try:
    p.set_option("SearchPath={{" + searchpath +"}}")

    # This means that formatting and other errors will raise an
    # exception. This simplifies our sample code, but is not
    # recommended for production code.
    p.set_option("errorpolicy=exception")
    p.set_option("charref=true");

    # Set an output path according to the name of the topic
    if (p.begin_document(outfile, "") == -1):
        raise PDFlibException("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_shaping")

    table = -1

    # Create table header
    row = 1
    col = 1
    for header in headers:
        if (col == 1):
            percentage = "10%"
        else:
            percentage = "45%"
        optlist = (
           "fittextline={fontname=Helvetica-Bold encoding=winansi fontsize=14} "
           "colwidth=" + percentage )
        table = p.add_table_cell(table, col, row, header, optlist)
        col += 1
        
    row += 1
    
    # Create shaping samples
    for shapingsample in shapingsamples:
        col=1

        # Column 1: language name
        optlist = "fittextline={fontname=Helvetica encoding=unicode fontsize=12}"
        table = p.add_table_cell(table, col, row, shapingsample["language"], optlist)

        col += 1

        # Column 2: raw text
        optlist = (
            "fontname={%s} encoding=unicode fontsize=13 "
            "leading=150%% alignment=left" %
                shapingsample["fontname"])
        tf = p.create_textflow(shapingsample["text"],optlist)
        optlist = "margin=4 fittextflow={verticalalign=top} textflow=%d" % tf
        table = p.add_table_cell(table, col, row, "", optlist)

        col += 1
        
        # Column 3: shaped and reordered text (Textline or Textflow)
        if (shapingsample["textflow"]):
            optlist = (
               "fontname={%s} encoding=unicode fontsize=13 %s "
               "leading=150%% alignment=left" %
                   (shapingsample["fontname"], shapingsample["optlist"]))
            tf = p.create_textflow(shapingsample["text"], optlist)
            optlist = "margin=4 fittextflow={verticalalign=top} textflow=%d" % tf
            table = p.add_table_cell(table, col, row, "", optlist)
        else:
            optlist = (
               "fittextline={fontname={%s} encoding=unicode "
               "fontsize=13 %s}" %
                   (shapingsample["fontname"], shapingsample["optlist"]))
            table = p.add_table_cell(table, col, row,
                     shapingsample["text"], optlist)
            
        row += 1

    # ---------- Place the table on one or more pages ----------
    #
    # Loop until all of the table is placed; create new pages
    # as long as more table instances need to be placed.
    result = "_boxfull"
    while (result == "_boxfull"):
        p.begin_page_ext(0, 0, "width=a4.height height=a4.width")

        # Shade every other row; draw lines for all table cells.
        optlist = "header=1 fill={{area=rowodd fillcolor={gray 0.9}}} stroke={{line=other}} "

        # Place the table instance
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
