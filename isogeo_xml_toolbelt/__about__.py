#! python3  # noqa: E265

"""
    Metadata about the package to easily retrieve informations.
    see: https://packaging.python.org/guides/single-sourcing-package-version/
"""

# standard library
from datetime import date

__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__license__",
    "__summary__",
    "__title__",
    "__uri__",
    "__version__",
]


__title__ = "Isogeo XML Toolbelt"
__summary__ = "Toolbelt to read, import and export metadata stored in XML according to the ISO standards 19139 and 19110."
__uri__ = "https://pypi.org/project/isogeo-xml-toolbelt/"

__version__ = "1.0.0"

__author__ = "Isogeo"
__email__ = "contact@isogeo.com"

__license__ = "GNU Lesser General Public License v3.0"
__copyright__ = "2016 - {0}, {1}".format(date.today().year, __author__)
