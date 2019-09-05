# coding: utf8
#! python3


# #############################################################################
# ###### Libraries #########
# ##########################

# Standard library
import logging
from pathlib import Path

# Isogeo XML toolbelt
from isogeo_xml_toolbelt.readers import MetadataIso19139
from isogeo_xml_toolbelt.reporters import CsvReporter

# Modules
from names_decoder.decode_name import decode_name

# environment vars
load_dotenv("orano.env", override=True)

# usage
csv_report = CsvReporter(
    csvpath=Path(".report_orano.csv"),
    headers=[
        "title",
        "abstract",
        "keywords",
        "country",
        "region",
        "date",
        "resolution",
        "scale",
        "contact",
        "organisation",
    ],
)

li_fixtures_xml = sorted(
    Path(
        r"/Users/LéoDARENGOSSE/ISOGEO/SIG - Documents/CLIENTS/85_ORANO/Echantillon"
    ).glob("**/*.xml")
)

for xml_path in li_fixtures_xml:
    md = MetadataIso19139(xml=xml_path)
    decode = decode_name(md.title, xml_path)

    # print (md.title)
    # contacts =

    for contact in md.list_contacts:
        name_contact = contact.get("name")
        organisation = contact.get("organisation")
    # print(md.asDict().get("title"), md.asDict().get("contacts"))

    d = {
        "title": md.title,
        "abstract": md.abstract.encode("utf-8"),
        "keywords": '|'.join(md.keywords), #list to char with delimeter "|"
        "date": md.date,
        "resolution": md.resolution,
        "scale": md.scale.replace(",", ""),
        "contact": name_contact,
        "organisation": organisation,
    }

    print(d)
    csv_report.add_unique(d)