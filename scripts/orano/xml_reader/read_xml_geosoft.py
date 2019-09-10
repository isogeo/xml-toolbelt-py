# -*- coding: UTF-8 -*-
#! python3

# #############################################################################
# ###### Libraries #########
# ##########################

# Standard library
import logging
from pathlib import Path
from os import environ
import chardet

# 3rd party
from dotenv import load_dotenv

# Isogeo XML toolbelt
from isogeo_xml_toolbelt.readers import MetadataIso19139
from isogeo_xml_toolbelt.reporters import CsvReporter

# ##############################################################################
# ############ Globals ############
# #################################

# environment vars
load_dotenv("./orano.env", override=True)

# logging
logging.basicConfig(
    format="%(asctime)s || %(levelname)s "
    "|| %(module)s || %(funcName)s || %(lineno)s "
    "|| %(message)s",
    level=logging.DEBUG,
)

# usage
csv_report = CsvReporter(
    csvpath=Path("scripts/orano/xml_reader/xml_reader_result.csv"),
    headers=[
        "title",
        "abstract",
        "keywords",
        "date",
        "resolution",
        "scale",
        "contact",
        "organisation",
    ],
)

print(environ.get("PATH_TO_ANALYSE"))

li_fixtures_xml = sorted(
    Path("/Users/LéoDARENGOSSE/ISOGEO/SIG - Documents/CLIENTS/85_ORANO/Echantillon").glob("**/*.xml")
)
for xml_path in li_fixtures_xml:
    md = MetadataIso19139(xml=xml_path)

    # print (md.title)
    # contacts =

    for contact in md.list_contacts:
        name_contact = contact.get("name")
        organisation = contact.get("organisation")
    # print(md.asDict().get("title"), md.asDict().get("contacts"))

    d = {
        "title": md.title,
        "abstract": md.abstract.encode("utf8"),
        "keywords": '|'.join(md.keywords), #list to char with delimeter "|"
        "date": md.date,
        "resolution": md.resolution.split("m")[0], #delete unity
        "scale": md.scale.replace(",", ""),
        "contact": name_contact,
        "organisation": organisation,
        "path": xml_path
    }

    # print(d)
    csv_report.add_unique(d)

    # print(xml_path.resolve(), test.storageType)
