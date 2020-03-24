'''
Load the CIOD macro tables from DICOM Standard PS3.3, Annex A.
All CIOD tables are defined in chapter A of the DICOM Standard.
Output the tables in JSON format, one entry per CIOD.
'''
import sys
import re

from dicom_standard import parse_lib as pl
from dicom_standard import parse_relations as pr
from dicom_standard.table_utils import (
    get_chapter_tables,
    tables_to_json,
    get_short_standard_link,
    get_table_description,
    table_to_dict,
)

CHAPTER_ID = 'chapter_A'
# Include optional "s" at end of "Functional Group" to catch Table A.32.9-2
TABLE_SUFFIX = re.compile(".*Functional Groups? Macros$")
COLUMN_TITLES = ['macro', 'section', 'usage']


def is_valid_macro_table(table_div):
    return TABLE_SUFFIX.match(pr.table_name(table_div))


def macro_table_to_dict(table):
    return table_to_dict(table, COLUMN_TITLES)


def get_table_with_metadata(table_with_tdiv):
    table, tdiv = table_with_tdiv
    clean_name = pl.clean_table_name(pr.table_name(tdiv))
    table_description = get_table_description(tdiv)
    return {
        'name': clean_name,
        'macros': table,
        'id': pl.create_slug(clean_name),
        'description': str(table_description),
        'linkToStandard': get_short_standard_link(tdiv)
    }


if __name__ == "__main__":
    standard = pl.parse_html_file(sys.argv[1])
    tables, tdivs = get_chapter_tables(standard, CHAPTER_ID, is_valid_macro_table)
    parsed_table_data = tables_to_json(tables, tdivs, macro_table_to_dict, get_table_with_metadata)
    pl.write_pretty_json(parsed_table_data)