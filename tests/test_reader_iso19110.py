# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:
    
    ```python
    python -m unittest tests.test_reader_iso19110
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from pathlib import Path
import sys
import unittest

# modules
from reader_iso19110 import MetadataIso19110

# #############################################################################
# ######## Globals #################
# ##################################

# ensure log and output dirs
Path("tests/logs").mkdir(exist_ok=True)
Path("tests/output").mkdir(exist_ok=True)

# #############################################################################
# ########## Classes ###############
# ##################################


class TestReaderIso19110(unittest.TestCase):
    """Test the XML ISO19110 reader."""

    # standard methods
    def setUp(self):
        """Executed before each test."""
        # fixtures
        self.li_fixtures_repo = sorted(Path(r"tests/fixtures/iso19110").glob("*.xml"))


    def tearDown(self):
        """Executed after each test."""
        pass

    #  -- Tests ------------------------------------------------------------
    def test_read(self):
        """Check reader"""
        # loop on fixtures
        for i in self.li_fixtures_repo:
            md = MetadataIso19110(str(i.resolve()))
            self.assertEqual(md.asDict().get("name"), md.name)
            self.assertEqual(md.asDict().get("title"), md.name)
            print(md.name)
