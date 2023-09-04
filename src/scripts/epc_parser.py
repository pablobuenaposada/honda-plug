import contextlib
import csv

from part.constants import SOURCE_EPC_4_00
from part.lambdas import add_part
from scrapper.utils import format_reference


def run(*args):
    """
    run: python src/manage.py runscript epc_parser --script-args data.csv
    """
    with open(args[0]) as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            with contextlib.suppress(Exception):
                add_part(format_reference(row[5]), SOURCE_EPC_4_00, f"row {row[0]}")
