# ISO 19139 - XML Fixer

Quicky script to fix missing information within XML files, according to the ISO 19139 standard.

## Usage

1. Create a folder  `input`
2. Put XML files into
3. Eventually customize the script:
    * set output values ([lines ~50](https://github.com/Guts/iso19139_xml_fixer/blob/97f8784a698df27ee7a3ccae1aeba0c4fbf4c7ac/md_xml_fixer.py#L50-L53))
    * enable/disable fixes to apply ([lines ~285](https://github.com/Guts/iso19139_xml_fixer/blob/97f8784a698df27ee7a3ccae1aeba0c4fbf4c7ac/md_xml_fixer.py#L285-L288))
4. Launch the script:

    ```py
    py -3 md_xml_fixer.py
    ```

5. New XML files are generated in the `output` folder.

## Credits

Script created for Brest Métropole, as a service executed by [Isogeo](https://github.com/isogeo/).
