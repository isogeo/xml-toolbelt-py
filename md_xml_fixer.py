#! python3
#! /usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

# -----------------------------------------------------------------------------
# Name:         Metadata XML fixer
# Purpose:      Check
# Python:       2.7.x
# Author:       Julien Moura (https://github.com/Guts)
# Created:      08/09/2017
# -----------------------------------------------------------------------------

# #############################################################################
# ###### Libraries #########
# ##########################

# Standard library
import logging
from logging.handlers import RotatingFileHandler
from os import getcwd, listdir, mkdir, path
import sys
from xml.dom import minidom
from xml.etree import ElementTree as ET

# imports depending on Python version
if (sys.version_info < (3, 0)):
    from io import open
else:
    pass

# ##############################################################################
# ############ Globals ############
# #################################

# LOG
logger = logging.getLogger("XML_ISO19139_FIXER")
logging.captureWarnings(True)
logger.setLevel(logging.DEBUG)
log_form = logging.Formatter("%(asctime)s || %(levelname)s "
                             "|| %(module)s || %(lineno)s || %(message)s")
logfile = RotatingFileHandler("LOG_XML_FIXER.log", "a", 5000000, 1)
logfile.setLevel(logging.DEBUG)
logfile.setFormatter(log_form)
logger.addHandler(logfile)
logger.info("Python version: {}"
            .format(sys.version_info))

# customize script
ds_creation_date = "2017-09-08"

# #############################################################################
# ########### Classes #############
# #################################


class MetadataXML19139Fixer(object):
    """ISO 19139 XML fixer."""

    def __init__(self):
        """Batch edit input XML files to enhance compliance to ISO19139."""
        self.check_folders()
        self.ns = self.add_namespaces()
        super(MetadataXML19139Fixer, self).__init__()

    def check_folders(self):
        """Check prerequisites."""
        self.fold_in = path.join(getcwd(), "input")
        self.fold_out = path.join(getcwd(), "output")
        # input folder
        if not path.isdir(self.fold_in):
            try:
                mkdir(self.fold_in, "0o777")
            except Exception as e:
                logger.error(e)
                sys.exit()
        else:
            logger.info("Input folder already exists.")
            pass

        # input XML files
        if not len(listdir(self.fold_in)):
            logger.error("Input folder was not created, so "
                         "there is not any XML file. Please "
                         "copy your XML ISO19139 files inside.")
            sys.exit()
        else:
            logger.info("Files are present in input folder.")

        # output folder
        if not path.isdir(self.fold_out):
            try:
                mkdir(self.fold_out, "0o777")
            except Exception as e:
                logger.error(e)
                sys.exit()
        else:
            logger.info("Output folder already exists.")
            pass
        # method ending
        return 0

    def add_namespaces(self):
        """Add ISO19139 namespaces."""
        ns = {"gts": "http://www.isotc211.org/2005/gts",
              "gml": "http://www.opengis.net/gml",
              "xsi": "http://www.w3.org/2001/XMLSchema-instance",
              "gco": "http://www.isotc211.org/2005/gco",
              "gmd": "http://www.isotc211.org/2005/gmd",
              "gmx": "http://www.isotc211.org/2005/gmx",
              "srv": "http://www.isotc211.org/2005/srv",
              "xl": "http://www.w3.org/1999/xlink"}

        # register namespaces
        for namespace in ns:
            ET.register_namespace(namespace, ns.get(namespace))
        return ns

    # -------- Methods to add missing XML parts ------------------------------

    def add_ds_creation_date(self):
        """Add metadata creation date into metadata XML.

        Under /MD_Metadata/identificationInfo/MD_DataIdentification/citation/CI_Citation/date):
        <date>
            <CI_Date>
                <date>
                    <gco:Date>2010-07-07Z</gco:Date>
                </date>
                <dateType>
                    <CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="creation">creation</CI_DateTypeCode>
                </dateType>
            </CI_Date>
        </date>
        """
        # date = ET.SubElement(elem, "<gmd:date>")
        ci_citation = self.get_md_ci_citation()
        # quicky way - NOT WORKING :'(
        # in_date = '''
        # <gmd:date gco="http://www.isotc211.org/2005/gco" gmd="http://www.isotc211.org/2005/gmd">
        #     <gmd:CI_Date>
        #         <gmd:date>
        #             <gco:Date>{}Z</gco:Date>
        #         </gmd:date>
        #         <gmd:dateType>
        #             <gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="creation">creation</gmd:CI_DateTypeCode>
        #         </gmd:dateType>
        #     </gmd:CI_Date>
        # </gmd:date>
        # '''.format(ds_creation_date)
        # ET.SubElement(ci_citation, in_date)

        # fastidious way - WORKING
        parent_date = ET.SubElement(ci_citation, "gmd:date")
        ci_date = ET.SubElement(parent_date, "gmd:CI_date")
        sub_date = ET.SubElement(ci_date, "gmd:date")
        # date value
        value_date = ET.SubElement(sub_date, "gco:date")
        value_date.text = "{}Z".format(ds_creation_date)
        # date type
        sub_date_type = ET.SubElement(ci_date, "gmd:dateType")
        sub_ci_date_typecode = ET.SubElement(sub_date_type, "gmd:CI_DateTypeCode")
        sub_ci_date_typecode.set("codeList", "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#CI_DateTypeCode")
        sub_ci_date_typecode.set("codeListValue", "creation")
        sub_ci_date_typecode.text = "creation"

    # -------- Methods to get XML parts --------------------------------------

    def get_identification_info(self):
        """Get XML main first levels items."""
        for i in self.tpl_root.findall('gmd:identificationInfo',
                                       self.ns):
            self.idenfo = i

        return self.idenfo

    def get_md_ci_citation(self):
        """Get CI_Citation level items."""
        pth_ci_citation = "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation"
        return self.tpl_root.find(pth_ci_citation,
                                  self.ns)

    # -------- XML utilis ----------------------------------------------------

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element."""
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

# #############################################################################
# ### Stand alone execution #######
# #################################

if __name__ == '__main__':
    """Test parameters for a stand-alone run."""
    app = MetadataXML19139Fixer()
    for xml in listdir(app.fold_in):
        logger.info(xml)
        # opening the input
        with open(path.join(app.fold_in, xml), 'r', encoding="utf-8") as in_xml:
            # parser
            app.tpl = ET.parse(in_xml)
            # getting the elements and sub-elements structure
            app.tpl_root = app.tpl.getroot()
            # creation date
            app.add_ds_creation_date()

            # # namespaces
            # for ns in app.ns:
            #     ET.register_namespace(ns, app.ns.get(ns))
            # saving the output xml file
            app.tpl.write(path.join(app.fold_out, xml),
                          encoding='utf-8',
                          xml_declaration=1,
                          # default_namespace=app.ns.get("gmd"),
                          method='xml')
