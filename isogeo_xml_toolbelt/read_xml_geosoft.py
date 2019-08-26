# Standard library
import logging
from pathlib import Path

# submodules
from csv_reporter import CsvReporter
from reader_iso19139 import MetadataIso19139

# logging
logging.basicConfig(format="%(asctime)s || %(levelname)s "
                            "|| %(module)s || %(funcName)s || %(lineno)s "
                            "|| %(message)s",
                    level=logging.DEBUG)

logging.debug("Standalone execution")

# usage
csv_report = CsvReporter(csvpath = Path("./scripts/orano/report_xml_orano.csv"),
                    headers=["title", "abstract", "keywords", "date", 
                            "resolution", "scale", "contact", "organisation"])

li_fixtures_xml = sorted(Path(r"/Users/LéoDARENGOSSE/ISOGEO\SIG - Documents/CLIENTS/85_ORANO/Echantillon").glob("**/*.xml"))
for xml_path in li_fixtures_xml:
    md = MetadataIso19139(xml=xml_path)
    
    # print (md.title)
    # contacts =

    for contact in md.list_contacts:
        name_contact = contact.get("name")
        organisation = contact.get("organisation")
    # print(md.asDict().get("title"), md.asDict().get("contacts"))
    
    d = {"title": md.title,
        "abstract": md.abstract,
        "keywords": md.keywords,
        "date": md.date,
        "resolution": md.resolution,
        "scale": md.scale.replace(",",""),
        "contact": name_contact,
        "organisation": organisation,
    }

    print(d)
    csv_report.add_unique(d)
   
    # print(xml_path.resolve(), test.storageType)

