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

# create csv
csv_report = CsvReporter(
    csvpath=Path("scripts/orano/report_orano.csv"),
    headers=[
        "name",
        "abstract",
        "keywords",
        "country",
        "region",
        "year",
        "date",
        "resolution",
        "scale",
        "contact",
        "organisation",
        "path",
    ],
)

#list xml files
li_fixtures_xml = sorted(
    Path(
        r"/Users/LéoDARENGOSSE/ISOGEO/SIG - Documents/CLIENTS/85_ORANO/Echantillon"
    ).glob("**/*.xml")
)

for xml_path in li_fixtures_xml:
    md = MetadataIso19139(xml=xml_path) # xml reader
    decode = decode_name(md.title, xml_path) # name decoder

    if decode.get("Main Theme") and decode.get("Main Theme") != "None":
        md.keywords.append(decode.get("Main Theme"))

    if decode.get("Theme 2") and decode.get("Theme 2") != "None":
        md.keywords.append(decode.get("Theme 2"))
    
    if decode.get("Theme 3") and decode.get("Theme 3") != "None":
        md.keywords.append(decode.get("Theme 3"))

    for contact in md.list_contacts:
        name_contact = contact.get("name")
        organisation = contact.get("organisation")

    d = {
        "name": decode.get("Name"),
        "abstract": md.abstract.encode("utf-8"),
        "keywords": '|'.join(md.keywords), #list to char with delimeter "|"
        "country": decode.get("Country"), 
        "region": decode.get("Region"),
        "year": decode.get("Year"),
        "date": md.date,
        "resolution": md.resolution.split("m")[0], #delete unity
        "scale": md.scale.replace(",", ""),
        "contact": name_contact,
        "organisation": organisation,
        "path": xml_path
    }

    print(d)
    csv_report.add_unique(d)