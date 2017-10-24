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
from datetime import datetime, date
from copy import deepcopy               # advanced copy
import logging
from logging.handlers import RotatingFileHandler
from os import getcwd, listdir, mkdir, path
import sys
from xml.dom import minidom
from xml.etree import ElementTree as ET

# Python 3 backported
from collections import OrderedDict

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

    # -------- Methods to add missing XML parts --------------------------------------

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

    def get_md_data_identification(self):
        """Get MD_DataIdentification level items."""
        return self.get_identification_info().find('gmd:MD_DataIdentification',
                                                   self.ns)

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

    # -------- LEGACY ----------------------------------------------------

    def iso19139(self, dest, dico_layer, dico_profil, blabla):
        u"""Export to xml file according to the ISO 19139."""
        # opening the template
        with open(r"data/xml/template_iso19139.xml", 'r')as iso:
            # parser
            template = ET.parse(iso)
            # namespaces
            namespaces = ET.register_namespace("gts", "http://www.isotc211.org/2005/gts")
            namespaces = ET.register_namespace("gml", "http://www.opengis.net/gml")
            namespaces = ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
            namespaces = ET.register_namespace("gco", "http://www.isotc211.org/2005/gco")
            namespaces = ET.register_namespace("gmd", "http://www.isotc211.org/2005/gmd")
            namespaces = ET.register_namespace("gmx", "http://www.isotc211.org/2005/gmx")
            namespaces = ET.register_namespace("srv", "http://www.isotc211.org/2005/srv")
            # getting the elements and sub-elements structure
            tpl_root = template.getroot()
            # transform coordinates to WGS84 for catalogs display
            if dico_layer.get('EPSG') != u'None':
                u""" if ogr found the ESPG code """
                srs84 = Transproj(epsg=int(dico_layer.get('EPSG')),
                                  Xmin=dico_layer.get('Xmin'),
                                  Ymin=dico_layer.get('Ymin'),
                                  Xmax=dico_layer.get('Xmax'),
                                  Ymax=dico_layer.get('Ymax')).tupwgs84
            else:
                u""" if not... """
                srs84 = (dico_layer.get('Xmin'),
                         dico_layer.get('Ymin'),
                         dico_layer.get('Xmax'),
                         dico_layer.get('Ymax'))
            # parsing and completing template structure
            for elem in tpl_root.getiterator():
                # universal identifier to know how the metadata has been created
                if elem.tag == '{http://www.isotc211.org/2005/gmd}fileIdentifier':
                    elem[0].text = "Metadator_" + \
                                   str(datetime.today()).replace(" ", "")\
                                                        .replace(":", "")\
                                                        .replace(".","-jm-")
                # EPSG code
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}code':
                    elem[0].text = dico_layer.get(u'srs') + u" (EPSG : " + unicode(dico_layer.get(u'EPSG')) + ")"
                    continue
                # standart projection EPSG
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}codeSpace':
                    elem[0].text = 'EPSG'
                    continue
                # title
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}title':
                    elem[0].text = dico_layer.get('title')
                    continue
                # spatial extension
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}westBoundLongitude':
                    elem[0].text = str(srs84[0])
    ##                elem[0].text = str(dico_layer['Xmin'])
                    continue
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}eastBoundLongitude':
                    elem[0].text = str(srs84[2])
    ##                elem[0].text = str(dico_layer['Xmax'])
                    continue
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}southBoundLatitude':
                    elem[0].text = str(srs84[1])
    ##                elem[0].text = str(dico_layer['Ymin'])
                    continue
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}northBoundLatitude':
                    elem[0].text = str(srs84[3])
    ##                elem[0].text = str(dico_layer['Ymax'])
                    continue
                # description
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}abstract':
                    elem[0].text = dico_profil['description']
                    continue
                # update rythm
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}status':
                    elem[0].attrib['codeListValue'] = dico_profil['rythm']
                    continue
                # infos descriptives
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}MD_DataIdentification':
                    infos = elem
                    mtc_them = infos[5]
                    mtc_geo = infos[6]
                    lg_don = infos[10]
                    continue
                # scale
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}MD_RepresentativeFraction':
                    scale = elem
                    scale[0][0].text = str(dico_profil.get('echelle'))
                    continue
                # distribution
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}MD_DigitalTransferOptions':
                    distrib = elem
                    siteweb = distrib[0][0]
                    siteweb[0][0].text = dico_profil.get('url')
                    siteweb[2][0].text = dico_profil.get('url_label')
                    continue
                # creation date
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}CI_Date' \
                and elem[1][0].attrib['codeListValue'] == 'creation':
                    elem[0][0].text = dico_layer.get(u'date_crea')
##                    crea = date.isoformat(datetime(crea[0], crea[1], crea[2]))
##                    elem[0][0].text = crea
                # last update
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}CI_Date' \
                and elem[1][0].attrib['codeListValue'] == 'revision':
                    elem[0][0].text = dico_layer.get(u'date_actu')
##                    reviz = date.isoformat(datetime(reviz[0], reviz[1], reviz[2]))
##                    elem[0][0].text = reviz
                # format
                elif elem.tag == '{http://www.isotc211.org/2005/gmd}MD_Format':
                    elem[0][0].text = 'ESRI Shapefile'

            tpl_cat = list(tpl_root)

            # metadata language
            lg_met = tpl_cat[1]
            list(lg_met)[0].text = dico_profil[u'lang_md']

            # data language
            list(lg_don)[0].text = dico_profil[u'lang_data']

            # metadata date
            tpl_cat[4][0].text = str(datetime.today())[:-7]

            # Contact
            ct_cont = tpl_cat[3][0]
            list(ct_cont)[0][0].text = dico_profil[u'cont_name']
            list(ct_cont)[1][0].text = dico_profil[u'cont_orga']
            list(ct_cont)[2][0].text = dico_profil[u'cont_role']
            cont_info = list(ct_cont)[3][0]
            cont_phone = list(cont_info)[0]
            list(cont_phone)[0][0][0].text = dico_profil['cont_phone']
            cont_adress = list(cont_info)[1]
            adress = list(cont_adress[0])[0]
            adress[0].text = dico_profil['cont_street']
            ville = list(cont_adress[0])[1]
            ville[0].text = dico_profil['cont_city']
            cp = list(cont_adress[0])[2]
            cp[0].text = dico_profil['cont_cp']
            pays = list(cont_adress[0])[3]
            pays[0].text = dico_profil['cont_country']
            mail = list(cont_adress[0])[4]
            mail[0].text = dico_profil['cont_mail']
            fonction = list(ct_cont)[4]
            fonction[0].attrib['codeListValue'] = dico_profil['cont_func']

            # Responsable
            ct_resp = list(infos[3][0])
            ct_resp[0][0].text = dico_profil[u'resp_name']
            ct_resp[1][0].text = dico_profil[u'resp_orga']
            ct_resp[2][0].text = dico_profil[u'resp_role']
            resp_info = list(ct_resp[3][0])
            resp_info[0][0][0][0].text = dico_profil[u'resp_phone']
            resp_adress = list(resp_info[1][0])
            resp_adress[0][0].text = dico_profil['resp_street']
            resp_adress[1][0].text = dico_profil['resp_city']
            resp_adress[2][0].text = dico_profil['resp_cp']
            resp_adress[3][0].text = dico_profil['resp_country']
            resp_adress[4][0].text = dico_profil['resp_mail']

            # thematics keywords
            for i in dico_profil.get('keywords'):
                infos.append(deepcopy(mtc_them))
            infos.remove(mtc_them)
            x = 0
            for tem in list(infos):
                if tem.tag == '{http://www.isotc211.org/2005/gmd}descriptiveKeywords' \
                and tem[0][1][0].attrib['codeListValue'] == 'theme':
                    tem[0][0][0].text = dico_profil.get('keywords')[x]
                    x = x+1

            # places keywords
            for i in dico_profil.get('geokeywords'):
                infos.append(deepcopy(mtc_geo))
            infos.remove(mtc_geo)
            y = 0
            for tem in list(infos):
                if tem.tag == '{http://www.isotc211.org/2005/gmd}descriptiveKeywords' \
                and tem[0][1][0].attrib['codeListValue'] == 'place':
                    tem[0][0][0].text = dico_profil.get('geokeywords')[y]
                    y = y+1

            # saving the xml file
            template.write(path.join(dest + "/{0}_MD.html".format(dico_layer['name'][:-4])),
                           encoding='utf-8',
                           xml_declaration='version="1.0"',
                           default_namespace=namespaces,
                           method='xml')
        # End of function
        return template

# #############################################################################
# ### Stand alone execution #######
# #################################

if __name__ == '__main__':
    """Test parameters for a stand-alone run."""
    app = MetadataXML19139Fixer()
    print(dir(app))
    for xml in listdir(app.fold_in):
        logger.info(xml)
        print(xml)
        # opening the input
        with open(path.join(app.fold_in, xml), 'r', encoding="utf-8") as in_xml:
            print(in_xml)
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
