/* $Id: starter_geospatial.java,v 1.5 2016/06/29 07:34:59 stm Exp $
 * Starter for georeferenced PDF:
 * Import an image with a map and add geospatial reference information
 *
 * Sample map and coordinates:
 * We use a map from www.openstreetmap.com; the geospatial coordinates of the
 * image edges were also provided by that Web site.
 * The coordinate system is WGS84 which is also used for GPS.
 *
 * Required software: PDFlib/PDFlib+PDI/PPS 9
 * Required data: image file and associated geospatial reference information
 */

package com.pdflib.cookbook.pdflib.geospatial;

import com.pdflib.pdflib;
import com.pdflib.PDFlibException;

class starter_geospatial {
    public static void main(String argv[]) {
        /* This is where the data files are. Adjust if necessary. */
        final String searchpath = "../input";
        final String outfile = "starter_geospatial.pdf";

        String pageoptlist;
        pdflib p = null;
        int image;
        final String imagefile = "munich.png";
        double mapwidth, mapheight;
        int exitcode = 0;

        /* WKT for plain latitude/longitude values in WGS84 */
        final String georefsystem = "worldsystem={type=geographic wkt={"
            + "GEOGCS[\"WGS 84\","
            + "  DATUM[\"WGS_1984\", SPHEROID[\"WGS 84\", 6378137,298.257223563]],"
            + "  PRIMEM[\"Greenwich\", 0.0],"
            + "  UNIT[\"Degree\", 0.01745329251994328]]"
            + "}} linearunit=M areaunit=SQM angularunit=degree";

        /* world coordinates of the image (in degrees) */
        double worldpoints[] = {
            48.145, /* latitude of top edge */
            11.565, /* longitude of left edge */
            11.59, /* longitude of right edge */
            48.13 /* latitude of bottom edge */
        };

        try {
            p = new pdflib();

            p.set_option("searchpath={" + searchpath + "}");

            /* This means we must check return values of load_font() etc. */
            p.set_option("errorpolicy=return");

            /* Start the document */
            if (p.begin_document(outfile, "compatibility=1.7ext3") == -1) {
                throw new Exception("Error: " + p.get_errmsg());
            }

            p.set_info("Creator", "PDFlib starter sample");
            p.set_info("Title", "starter_geospatial $Revision: 1.5 $");

            /* Load the map image */
            image = p.load_image("auto", imagefile, "");
            if (image == -1)
            {
                System.err.println("Error: " + p.get_errmsg());
                System.exit(2);
            }

            /* Retrieve image width and height */
            mapwidth = p.info_image(image, "imagewidth", "");
            mapheight = p.info_image(image, "imageheight", "");

            /* Generate georeference option list */
            pageoptlist = "";
            pageoptlist += "viewports={{ georeference={";
            pageoptlist += georefsystem + " ";

            /* Use the four corners as reference points; (0,0)=lower left etc. */
            pageoptlist += "mappoints={0 0  1 0  1 1  0 1} ";

            /*
             * The following can be used as a workaround for a problem with the
             * Avenza PDF Maps app on Android; otherwise the (almost) default
             * bounds values can be skipped:
             *
             * pageoptlist += "bounds={0.000001 0 0 1 1 1 1 0} ";
             */

            pageoptlist += "worldpoints={";

            /* lower left corner */
            pageoptlist += worldpoints[3] + " " + worldpoints[1] + " ";
            /* lower right corner */
            pageoptlist += worldpoints[3] + " " + worldpoints[2] + " ";
            /* upper right corner */
            pageoptlist += worldpoints[0] + " " + worldpoints[2] + " ";
            /* upper left corner */
            pageoptlist += worldpoints[0] + " " +  worldpoints[1] + " ";

            pageoptlist += "} } ";

            pageoptlist += "boundingbox={0 0 ";
            pageoptlist += mapwidth + " " + mapheight;
            pageoptlist += "} } }";

            /* Create a page with geospatial reference information. */
            p.begin_page_ext(mapwidth, mapheight, pageoptlist);

            /* Place the map on the lower left corner of the page */
            String optlist = "adjustpage boxsize={";
            optlist += mapwidth + " " + mapheight;
            optlist += "}";
            p.fit_image(image, 0, 0, optlist);

            p.end_page_ext("");

            p.end_document("");
        }
        catch (PDFlibException e) {
            System.err.print("PDFlib exception occurred:\n");
            System.err.print("[" + e.get_errnum() + "] " + e.get_apiname()
                    + ": " + e.get_errmsg() + "\n");
            exitcode = 1;
        }
        catch (Exception e) {
            System.err.println(e.getMessage());
            exitcode = 1;
        }
        finally {
            if (p != null) {
                p.delete();
            }
            System.exit(exitcode);
        }
    }
}
