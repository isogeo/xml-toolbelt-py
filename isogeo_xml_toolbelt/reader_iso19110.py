# -*- coding: utf-8 -*-
#! python3

"""
    Isogeo XML Fixer - Metadata

    Purpose:     Read a metadata stored into XML ISO 19110 as an object
    Authors:     Isogeo, inspired by the work did by GeoBretagne on mdchecker
    Python:      3.6.x
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import datetime
import logging
import os
from pathlib import Path
from uuid import UUID

# 3rd party library
import arrow
from lxml import etree

# #############################################################################
# ########## Globals ###############
# ##################################

# required subfolders
input_dir = Path("input/").mkdir(exist_ok=True)

# logging
logging.basicConfig(level=logging.INFO)


# #############################################################################
# ########## Functions #############
# ##################################
def xmlGetTextNodes(doc: etree._ElementTree, xpath: str, namespaces: dict):
    """Shorthand to retrieve serialized text nodes matching a specific xpath.

    :param lxml.etree._ElementTree doc: XML element to parse
    :param str xpath: Xpath to reach
    :param dict namespaces: XML namespaces like `lxml.etree.getroot().nsmap`
    """
    return ", ".join(doc.xpath(xpath, namespaces=namespaces))


def parse_string_for_max_date(dates_as_str: str):
    """Parse string with multiple dates to extract the most recent one. Used
    to get the latest modification date.

    :param str dates_as_str: string containing dates
    """
    try:
        dates_python = []
        for date_str in dates_as_str.split(","):
            date_str = date_str.strip()
            if date_str != "":
                date_python = arrow.get(date_str)
                dates_python.append(date_python)
        if len(dates_python) > 0:
            return max(dates_python)
    except:
        logging.error("date parsing error : " + dates_as_str)
        return None

# #############################################################################
# ########## Classes ###############
# ##################################
class MetadataIso19110(object):
    """Object representation of a metadata stored into XML respecting ISO 19110."""

    def __init__(self, xml: Path):
        """Read and  store the input XML metadata as an object.

        :param pathlib.Path xml: path to the XML file
        """
        # lxml needs a str not a Path
        if isinstance(xml, Path):
            self.xml_path = str(xml.resolve())
        else:
            raise TypeError("XML path must be a pathlib.Path instance.")
        # set nampespaces
        self.namespaces = {'gco': 'http://www.isotc211.org/2005/gco',
                           'geonet': 'http://www.fao.org/geonetwork',
                           'gfc': 'http://www.isotc211.org/2005/gfc',
                           'gmd': 'http://www.isotc211.org/2005/gmd',
                           'gml': 'http://www.opengis.net/gml',
                           'gmx': 'http://www.isotc211.org/2005/gmx',
                           'gts': 'http://www.isotc211.org/2005/gts',
                           'srv': 'http://www.isotc211.org/2005/srv',
                           'xlink': 'http://www.w3.org/1999/xlink',
                           'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
        # parse xml
        self.md = etree.parse(self.xml_path)
        # identifiers
        self.filename = xml.name
        try:
            self.fileIdentifier = UUID(xml.name)
        except ValueError:
            pass
        # name <--> equivalent to title
        self.name = xmlGetTextNodes(
            self.md,
            "/gfc:FC_FeatureCatalogue/gfc:name/gco:CharacterString/text()",
            self.namespaces)
        # field of application
        self.fieldOfapplication = xmlGetTextNodes(
            self.md,
            "/gfc:FC_FeatureCatalogue/gfc:fieldOfApplication/gco:CharacterString/text()",
            self.namespaces)

        # organization
        self.OrganisationName = xmlGetTextNodes(
            self.md,
            "/gfc:FC_FeatureCatalogue/gfc:producer/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text()",
            self.namespaces)


        # version date or datetime
        dates_str = xmlGetTextNodes(
            self.md,
            "/gfc:FC_FeatureCatalogue/gfc:versionDate/gco:Date/text()",
            self.namespaces)
        datetimes_str = xmlGetTextNodes(
            self.md,
            "/gfc:FC_FeatureCatalogue/gfc:versionDate/gco:DateTime/text()",
            self.namespaces)
        if dates_str != "":
            self.date = parse_string_for_max_date(dates_str)
        else:
            self.date = parse_string_for_max_date(datetimes_str)
        
        # contacts
        self.contact = {
            "email": self.md.xpath(
                "/gfc:FC_FeatureCatalogue/gfc:producer/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString/text()",
                namespaces=self.namespaces),
            "address": self.md.xpath(
                "/gfc:FC_FeatureCatalogue/gfc:producer/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString/text()",
                namespaces=self.namespaces),
            "postalCode": self.md.xpath(
                "/gfc:FC_FeatureCatalogue/gfc:producer/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString/text()",
                namespaces=self.namespaces),
            "city": self.md.xpath(
                "/gfc:FC_FeatureCatalogue/gfc:producer/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString/text()",
                namespaces=self.namespaces)
        }

        # feature types
        self.featureTypes = xmlGetTextNodes(
            self.md,
            "/gfc:FC_FeatureCatalogue/gfc:featureType/gfc:FC_FeatureType/gfc:typeName/gco:LocalName/text()",
            self.namespaces)
        self.featureAttributes = xmlGetTextNodes(
            self.md,
            "/gfc:FC_FeatureCatalogue/gfc:featureType/gfc:FC_FeatureType/gfc:carrierOfCharacteristics[6]/gfc:FC_FeatureAttribute/gfc:memberName/gco:LocalName/text()",
            self.namespaces)


    def __repr__(self):
        return self.fileIdentifier
        
    def __str__(self):
        return self.fileIdentifier
    
    def asDict(self):
        """Return the metadata object as a dict."""
        return {
            "filename": self.filename,
            #"fileIdentifier": self.fileIdentifier,
            "name": self.name,
            "title": self.name,
            "fieldOfApplication": self.fieldOfapplication,
            "date": self.date,
            "OrganisationName": self.OrganisationName,
            "contact": self.contact,
            "featureTypes": self.featureTypes
        }


# #############################################################################
# ### Stand alone execution #######
# #################################

if __name__ == "__main__":
    """Test parameters for a stand-alone run."""
    li_fixtures_xml = sorted(Path(r"tests/fixtures").glob("**/*.xml"))
    li_fixtures_xml += sorted(Path(r"input/CD92/Catalogue d'attribut").glob("**/*.xml"))
    for xml_path in li_fixtures_xml:
        test = MetadataIso19110(xml=xml_path)
        print(test.name,
              test.featureAttributes)
