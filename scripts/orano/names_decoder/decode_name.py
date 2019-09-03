# -*- coding: utf-8 -*-
#! python3

"""
    Isogeo - Orano's names Decoder
    Purpose:     Parse a folder containing exported metadata from Orano
    and decode file's name with Axinite's configuration (Software by Orano used to code filenames).
    Authors:     Isogeo
    Python:      3.7.x
"""
# ##############################################################################
# ########## Libraries #############
# ##################################

import xml.etree.ElementTree as ET
import logging
import csv
import os.path

# #############################################################################
# ######## Intialize log #################
# ##################################
logging.basicConfig(
    filename="log.log",
    format="%(asctime)s || %(funcName)s || %(levelname)s || %(message)s",
    level=logging.DEBUG,
)


def list_filenames_xml_from_directory(path: str) -> list:

    # #############################################################################
    # ######## Extract XML filenames from a path #################
    # ##################################

    list_filenames_xml = []
    counter = 0
    for root, dirs, files in os.walk(path):
        for i in files:
            ext = os.path.splitext(i)[1]  # get extension
            if ext == ".xml":  # get only xml files
                counter += 1
                name = i.split(".")[0]  # get name without extension
                list_filenames_xml.append({"name": name, "path": os.path.join(root, i)})

    logging.info("{} XML filenames founded in {}".format(counter, path))

    return list_filenames_xml


def decode_name(name: str, config: str, path: str) -> dict:

    # #############################################################################
    # ######## Intialize variable #################
    # ##################################

    name_country = None
    name_region = None
    name_maintheme = None
    year = None
    name_scale = None
    name_theme2 = None
    name_theme3 = None

    # #############################################################################
    # ######## Extract content from string name #################
    # ##################################
    logging.info("Split name : {}".format(name))

    code_country = name[0:2]
    if (
        code_country == "GA"
    ):  # exception for Gabon GA_C__KAYA_XX_XXXX_XXXXX_____01 → Country = Gabon Region = C_KAYA_KAYA
        code_region = name[3:10]
        code_maintheme = name[11:13]
        try:
            # verify year format and date
            number = int(name[14:18])
            if number >= 1900 and number <= 2100:
                year = number
                logging.info("Year = {}".format(year))
        except:
            logging.error("No Year found")
        code_scale = name[19:24]
        code_theme2 = name[25:27]
        code_theme3 = name[27:29]
        logging.warning("Gabon exception : Region's code will containt 6 characters. ")
    else:
        code_region = name[3:7]
        code_maintheme = name[8:10]
        try:
            # verify year format and date
            number = int(name[11:15])
            if number >= 1900 and number <= 2100:
                year = number
                logging.info("Year = {}".format(year))
        except:
            logging.error("No Year found")
        code_scale = name[16:21]
        code_theme2 = name[22:24]
        code_theme3 = name[24:26]

    # #############################################################################
    # ######## Parse configuration XML #################
    # ##################################

    tree = ET.parse(config)
    root = tree.getroot()
    countries = root[0]
    mainthemes = root[1]
    scales = root[2]

    # #############################################################################
    # ######## Search Country and Region #################
    # ##################################
    logging.info("Search Country and Region...")
    for country in countries:
        if code_country == country.get("code"):
            name_country = country.get("desc")
            regions = country[0]
            for region in regions:
                if code_region == region.get("code"):
                    name_region = region.get("desc")
                    break
            break

    if name_country:
        logging.info("Country = {}".format(name_country))
    else:
        logging.error("No country found")

    if name_region:
        logging.info(
            "Country {} an Region {} have been extracted.".format(
                name_country, name_region
            )
        )
    else:
        logging.error("No region found")

    # #############################################################################
    # ######## Search Mainthemes and SubThemes #################
    # ##################################
    logging.info("Search Main theme and Subtheme(s)...")
    if code_country == "GA":  # Gabon exception
        for maintheme in mainthemes:
            if code_maintheme == maintheme.get("code"):
                name_maintheme = maintheme.get("desc")
                logging.info("Main theme is :  {} ".format(name_maintheme))
                for subtheme in maintheme:
                    if code_theme2 == subtheme.get("code"):
                        name_theme2 = subtheme.get("desc")
                        logging.info("Theme 2 is : {}".format(name_theme2))
                    elif code_theme3 == subtheme.get("code"):
                        name_theme3 = subtheme.get("desc")
                    elif name[25:28] == subtheme.get(
                        "code"
                    ):  # Subtheme exceptions (when theme 2 composed by 3 characters)
                        logging.warning(
                            "Theme 2 containt 3 characters, so  there is no theme 3"
                        )
                        name_theme2 = subtheme.get("desc")
                        code_theme2 = name[25:28]
                    elif name[25:29] == subtheme.get(
                        "code"
                    ):  # Subtheme exceptions (when theme 2 composed by 4 characters)
                        logging.warning(
                            "Theme 2 containt 4 characters, so there is no theme 3"
                        )
                        name_theme2 = subtheme.get("desc")
                        code_theme2 = name[25:29]

    else:
        for maintheme in mainthemes:
            if code_maintheme == maintheme.get("code"):
                name_maintheme = maintheme.get("desc")
                for subtheme in maintheme:
                    if code_theme2 == subtheme.get("code"):
                        name_theme2 = subtheme.get("desc")
                    elif code_theme3 == subtheme.get("code"):
                        name_theme3 = subtheme.get("desc")
                    elif name[22:25] == subtheme.get(
                        "code"
                    ):  # Subtheme exceptions (when theme 2 composed by 3 characters)
                        logging.warning(
                            "Theme 2 containt 3 characters, so there is no theme 3"
                        )
                        name_theme2 = subtheme.get("desc")
                        code_theme2 = name[22:25]
                    elif name[22:26] == subtheme.get(
                        "code"
                    ):  # Subtheme exceptions (when theme 2 composed by 4 characters)
                        logging.warning(
                            "Theme 2 containt 4 characters, so there is no theme 3"
                        )
                        name_theme2 = subtheme.get("desc")
                        code_theme2 = name[22:26]

    if name_maintheme:
        logging.info("Main theme = {}".format(name_maintheme))
    else:
        logging.error("No Main theme found")

    if name_region:
        logging.info(
            "Main theme is {} and Subtheme(s) are {} and {} ".format(
                name_maintheme, name_theme2, name_theme3
            )
        )
    else:
        logging.error("No Theme 2 found")

    # #############################################################################
    # ######## Search scale #################
    # ##################################
    logging.info("Search Scale...")
    for scale in scales:
        if code_scale == scale.get("code"):
            name_scale = scale.get("desc")

    if name_scale:
        logging.info("Scale is {} ".format(name_scale))
    else:
        logging.error("No Scale found")

    result = {
        "Name": name,
        "Country": name_country,
        "Region": name_region,
        "Main Theme": name_maintheme,
        "Year": year,
        "Scale": name_scale,
        "Theme 2": name_theme2,
        "Theme 3": name_theme3,
        "Path": path,
    }

    logging.info("Extraction finished, result is {}".format(result))

    return result


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":

    config = "axinite.xml"
    path = "\\Users\LéoDARENGOSSE\ISOGEO\SIG - Documents\CLIENTS\85_ORANO\Echantillon"

    # write csv with decodage result
    with open("result.csv", "w", newline="") as csvfile:
        fieldnames = [
            "Name",
            "Country",
            "Region",
            "Main Theme",
            "Year",
            "Scale",
            "Theme 2",
            "Theme 3",
            "Path",
        ]

        csv.register_dialect("semicolon", delimiter=";")  # create dialect

        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, dialect="semicolon"
        )  # write csv with a dictionnary
        writer.writeheader()  # write header

        list_names_path = list_filenames_xml_from_directory(path)  # list names

        counter_csv = 0
        counter_undecodable = 0
        for dict_name_path in list_names_path:
            name = dict_name_path.get("name")
            path = dict_name_path.get("path")
            result = decode_name(name, config, path)
            country = result.get("Country")
            if (
                country is None
            ):  # if the country can't be found, the name might be undecodable
                logging.error(
                    "Name {} might be undecodable and will no be added to CSV Result".format(
                        result.get("Name")
                    )
                )
                counter_undecodable += 1
            else:
                writer.writerow(result)  # add result dictionary to csv
                logging.info("Add {} to CSV Result".format(result.get("Name")))
                counter_csv += 1

    logging.info(
        "{} filenames have been added to CSV Result, {} not.".format(
            counter_csv, counter_undecodable
        )
    )
