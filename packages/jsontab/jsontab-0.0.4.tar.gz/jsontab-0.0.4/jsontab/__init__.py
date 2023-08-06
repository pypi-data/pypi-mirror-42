"""Agnostically load JSON or tabular data

Functions
---------
from_json
    load a pandas DatFrame from data in JSON format

from_json_or_tab
    load a pandas DataFrame from data that may be in either JSON or tabular
    format
"""

from jsontab.jsontab import from_json, from_json_or_tab
