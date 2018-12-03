# -*- coding: utf-8 -*-
#! python3


"""
    Isogeo XML Fixer - Mover from GeoSource ZIP

    Purpose:     Parse a folder containing exported metadata from GeoSource
    and rename files qualifying by XML type and title.
    Authors:     Isogeo
    Python:      3.6.x

    ###############################################################################
    # Le script copie les fichiers metadata.xml dans un répertoire de destination #
    # et les renomme avec l'identifiant et le titre de la métadonnée              #
    ###############################################################################

    Ossature des exports Geosource :
    export-full-1542728453496
        Fiche
            0aad7122-baa3-42b4-8d79-cf9c3e83035c
            metadata	
                        metadata.xml
                  private
            public
                  info.xml
        Catalogue d’attribut
            0a80da9e-c5dc-4343-97fa-b6d5e05dfa9e
            metadata	
                        metadata.xml
                  private
            public
                  info.xml
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
from os import path, rename, walk
import shutil
from pathlib import Path
from uuid import UUID

# 3rd party library
import click
from lxml import etree

# #############################################################################
# ########## Globals ###############
# ##################################

# required subfolders
input_dir = Path("input/").mkdir(exist_ok=True)
input_dir = Path("output/").mkdir(exist_ok=True)

# logging
logging.basicConfig(level=logging.INFO)

path_src = path.realpath(r"C:\Users\leo.darengosse\Documents\Clients\CD 92\metadonnees_cd92\Fiche") #source path 
path_dest = path.realpath(r"C:\Users\leo.darengosse\Documents\Clients\CD 92\metadonnees_cd92_xml\Fiche") #destination path

# #############################################################################
# ########## Functions #############
# ##################################
def list_metadata_folder(folder: str, kind: str = "geosource") -> tuple:
    """TO DOC
    """
    li_metadata_folders = []
    # parse folder structure
    for subfolder in folder.glob("**"):
        # if foldername is a valid UUID, it's a geosource subfolder
        try:
            UUID(subfolder.name)
        except ValueError:
            continue
        # check if required subfolders are present
        if not check_folder_structure(subfolder):
            continue
        # append to the list
        li_metadata_folders.append(subfolder.resolve())
    return tuple(li_metadata_folders)


def check_folder_structure(folder: str, kind: str = "geosource") -> bool:
    """TO DOC
    """
    subfolders = [x.name for x in folder.iterdir() if x.is_dir()]
    return set(["metadata", "private", "public"]).issubset(subfolders)

def guess_19110_or_19139(folder: str) -> str:
    """TO DOC
    """
    # get info file
    info_path = folder / "info.xml"
    if not info_path.is_file():
        return "Info file not found. Unable to guess"

    # read info.xml
    info_xml = etree.parse(str(info_path))
    return info_xml.xpath("/info/general/schema/text()")[0]

############################################################################
# Cette fonction permet de récupérer le titre de la metadonnée dans le XML # 
############################################################################

def find_md_title(metadata):
    """TP DOC
    <gmd:identificationInfo>
        <gmd:MD_DataIdentification gco:isoType="gmd:MD_DataIdentification">
            <gmd:citation>
            <gmd:CI_Citation>
                <gmd:title>
                <gco:CharacterString>Axe de Seine et points kilométriques (SEINE_AXE)</gco:CharacterString>
            </gmd:title>
    """
    tree = ET.parse(metadata)  
    # getting the elements and sub-elements structure
    root = tree.getroot()

    ns = {"gmd": "http://www.isotc211.org/2005/gmd"} 

    pth_character_set = "gmd:identificationInfo/"\
                            "gmd:MD_DataIdentification/"\
                                "gmd:citation/"\
                                "gmd:CI_Citation/"\
                                "gmd:title/"
      
    
    result = root.find(pth_character_set, ns)
    
    if result is None:
      title = "no_title"
    else:       
      title = result.text

    title = title.replace(":","-")
    title = title.replace("/","-") # a ameliorer (commme dans isogeo2office par exemple)
    title = title.replace("&","-")
    # title = title.replace("/"," ")
    # title = title.replace("/"," ")
    # print(result.text)
      
    return title

#################################################
# Recherche, copie et renommage des fichier XML # 
#################################################


# def xml_renamer_mover(folder: str, kind: str = "geosource") -> bool:
#     """TO DOC
#     """
#     counter=0
#     for dirName, subdirList, fileList in walk(path_src): #browse files and subdirectories
#         # print('Found directory: %s' % dirName) 
#         for fname in fileList: #browse file's list
#             # print('\t%s' % fname)
#             ext = path.splitext(path.join(dirName, fname))[1] #get extension
#             # print(ext)

#             if fname == "metadata.xml" and "metadata" in dirName : #Two execeptions : d0f9d920-d5c5-4100-88ea-54c5005099b6\applschema\metadata.xml | 6b59fdc4-8923-4eb9-a75a-2c6c83dd59b0\metadata\metadata.iso19139.xml
#                 counter+=1   
#                 tree = ET.parse(fname)  
#                 root = tree.getroot() 
                        
#                 # print(dirName)

#                 md_id = path.split(path.dirname(dirName))[1] #get metadata id ffdba339-5877-4ffb-b558-1b6551704357 from C:\...\Fiche\ffdba339-5877-4ffb-b558-1b6551704357\metadata
                
#                 source_md = path.join(dirName, fname) #get md
#                 shutil.copy(source_md, path_dest) #copy md to destination path
                
#                 dest_md = path.join(path_dest, fname) 

#                 md_title = find_md_title(source_md)
#                 # print (md_title)

#                 rename(dest_md, path.join(path_dest, md_id +"_"+ md_title + ext)) #rename md in destination folder
                
#                 # print(md_id)
#                 # print(path.join(dirName,fname))
#                 # print(path.join(path_dest, md_id + ext))
                
#     print(counter) # to check number of metadatas

# #############################################################################
# ####### Main function ###########
# #################################
@click.command()
@click.argument("input_dir", default=r"input")
@click.argument("output_dir", default=r"ouput")
def cli_switch_from_geosource(input_dir, output_dir):
    input_folder = Path(input_dir)
    if not input_folder.exists():
        raise IOError("Input folder doesn't exist.")
    # get list of metadata
    li_metadata = list_metadata_folder(input_folder)
    print(len(li_metadata))
    # guess if it's a 19110 or a 19139 metadata
    for i in li_metadata:
        print(guess_19110_or_19139(i), i)
        

# #############################################################################
# ### Stand alone execution #######
# #################################

if __name__ == "__main__":
    """Test parameters for a stand-alone run."""
    cli_switch_from_geosource()
