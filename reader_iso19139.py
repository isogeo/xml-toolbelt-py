# -*- coding: utf-8 -*-
#! python3


"""
    Isogeo XML Fixer - Metadata

    Purpose:     Read a metadata stored into XML ISO 19139 as an object
    Authors:     First work by GeoBretagne on mdchecker - updated by Isogeo
    Python:      3.6.x
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import datetime
import hashlib
import json
import logging
import os
from pathlib import Path

# 3rd party library
import arrow
from lxml import etree
import dateutil.parser

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
def xmlGetTextNodes(doc, xpath, namespaces):
    """
    Shorthand to retrieve serialized text nodes matching a specific xpath
    """
    return ", ".join(doc.xpath(xpath, namespaces={
        "gmd": "http://www.isotc211.org/2005/gmd",
        "gco": "http://www.isotc211.org/2005/gco"
    }))


def parse_string_for_max_date(dates_as_str):
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
        logging.error("date parsing error : " +dates_as_str)
        return None

# #############################################################################
# ########## Classes ###############
# ##################################
class MetadataIso19139:
    """
    metadata with unit test methods
    """
    def __init__(self, xml):
        self.namespaces = {
            "gmd": "http://www.isotc211.org/2005/gmd",
            "gco": "http://www.isotc211.org/2005/gco"
        }
        self.bbox = []
        self.xml = xml
        self.md = etree.parse(xml)
        self.fileIdentifier = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString/text()",
            self.namespaces)
        self.MD_Identifier = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:identificationInfo/"
            "gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/"
            "gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()",
            self.namespaces)
        self.title = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:identificationInfo/"
            "gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/"
            "gmd:title/gco:CharacterString/text()",
            self.namespaces)
        self.OrganisationName = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:identificationInfo/"
            "gmd:MD_DataIdentification/gmd:pointOfContact/"
            "gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text()",
            self.namespaces)
        self.abstract = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:identificationInfo/"
            "gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString/text()",
            self.namespaces)

        # date or datetime ?
        dates_str = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:identificationInfo/"
            "gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/"
            "gmd:date/gmd:CI_Date/gmd:date/gco:Date/text()",
            self.namespaces)
        datetimes_str = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:identificationInfo/"
            "gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/"
            "gmd:date/gmd:CI_Date/gmd:date/gco:DateTime/text()",
            self.namespaces)
        if dates_str != "":
            self.date = parse_string_for_max_date(dates_str)
        else:
            self.date = parse_string_for_max_date(datetimes_str)
        
        # seems always datetime
        md_dates_str = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:dateStamp/"
            "gco:DateTime/text()",
            self.namespaces)
        self.md_date = parse_string_for_max_date(md_dates_str)
        self.contact = {
            "mails": self.md.xpath(
                "/gmd:MD_Metadata/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/"
                "gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString/text()",
                namespaces=self.namespaces)
        }
        try:
            self.lonmin = float(xmlGetTextNodes(
                self.md,
                "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/"
                "gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/"
                "gmd:westBoundLongitude/gco:Decimal/text()",
                self.namespaces))
            self.lonmax = float(xmlGetTextNodes(
                self.md,
                "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/"
                "gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/"
                "gmd:eastBoundLongitude/gco:Decimal/text()",
                self.namespaces))
            self.latmin = float(xmlGetTextNodes(
                self.md,
                "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/"
                "gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/"
                "gmd:southBoundLatitude/gco:Decimal/text()",
                self.namespaces))
            self.latmax = float(xmlGetTextNodes(
                self.md,
                "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/"
                "gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/"
                "gmd:northBoundLatitude/gco:Decimal/text()",
                self.namespaces))
        except:
            self.lonmin = -180
            self.lonmax = 180
            self.latmin = -90
            self.latmax = 90

        # SRS
        self.srs = xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/"
            "gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString/text()",
            self.namespaces)
        self.srs += xmlGetTextNodes(
            self.md,
            "/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/"
            "gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString/text()",
            self.namespaces)
        

    def __repr__(self):
        return self.fileIdentifier
        
    def __str__(self):
        return self.fileIdentifier
    
    def asDict(self):
        return {
            "fileIdentifier": self.fileIdentifier,
            "MD_Identifier": self.MD_Identifier,
            "md_date": self.md_date,
            "title": self.title,
            "OrganisationName": self.OrganisationName,
            "abstract": self.abstract,
            "date": self.date,
            "contact": self.contact,
            "srs": self.srs,
            "latmin": self.latmin,
            "latmax": self.latmax,
            "lonmin": self.lonmin,
            "lonmax": self.lonmax
        }
        

# #############################################################################
# ### Stand alone execution #######
# #################################

if __name__ == "__main__":
    """Test parameters for a stand-alone run."""
    li_fixtures_xml = sorted(Path(r"tests/fixtures").glob("**/*.xml"))
    li_fixtures_xml += sorted(Path(r"input").glob("**/*.xml"))
    for xml in li_fixtures_xml:
        test = MetadataIso19139(xml=os.path.normpath(xml))
        print(test.asDict().get("title"), test.asDict().get("srs"))
