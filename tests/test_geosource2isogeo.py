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
from pathlib import Path
from uuid import UUID

# 3rd party library
from lxml import etree

# # test info from info.xml
# folder = Path(
#     r"tests/fixtures/geosource_cd94/1b8ccc26-99f4-455b-bb9c-ead396af50fa")
# info_path = folder / "info.xml"
# info_xml = etree.parse(str(info_path))
# l_files_pub = info_xml.xpath("/info/public/file")
# print(len(l_files_pub), l_files_pub[0].get("name"))

# l_files_priv = info_xml.xpath("/info/private/file")
# print(len(l_files_priv), l_files_priv[0].get("name"))


# l_files = [Path(folder / "public" / x.get("name"))
#            for x in l_files_pub
#            if Path(folder / "public" / x.get("name")).is_file()]
# l_files.extend([Path(folder / "private" / x.get("name"))
#                 for x in l_files_priv
#                 if Path(folder / "private" / x.get("name")).is_file()])

# print(l_files)
