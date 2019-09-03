import xml.etree.ElementTree as ET

tree = ET.parse("axinite.xml")
root = tree.getroot()
countries = root[0]
mainthemes = root[1]
scales = root[2]

# #############################################################################
# ######## Research exceptions in Axinite configuration #################
# ##################################


##countries
# for country in countries:
#     code_country = country.get('code')
#     if len(code_country) != 2:
#         name_country = country.get('desc')
#         print(name_country, code_country)

##regions
# for country in countries:
#     name_country = country.get('desc')
#     regions = country[0]
#     for region in regions:
#         code_region = region.get('code')
#         name_region = region.get('desc')
#         if len(code_region) != 4:
#             print(name_country, len(code_region), code_region, name_region)

##maintheme
# for maintheme in mainthemes:
#     name_maintheme = maintheme.get('desc')
#     code_maintheme = maintheme.get('code')
#     if len(code_maintheme) != 2:
#         print(name_maintheme, len(code_maintheme), code_maintheme)

# for maintheme in mainthemes:
#     name_maintheme = maintheme.get('desc')
#     code_maintheme = maintheme.get('code')
#     subthemes = list()
#     for subtheme in maintheme:
#         code_theme = subtheme.get('code')
#         name_theme  = subtheme.get('desc')
#         if len(code_theme) == 4:
#             print(name_maintheme + "," + code_theme + "," + name_theme)

# scales
for scale in scales:
    name_scale = scale.get("desc")
    code_scale = scale.get("code")
    if len(code_scale) != 2:
        print(name_scale, len(code_scale), code_scale)
