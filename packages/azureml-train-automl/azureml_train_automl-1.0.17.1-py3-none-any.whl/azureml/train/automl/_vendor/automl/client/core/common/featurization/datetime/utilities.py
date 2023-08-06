# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilites for datatime module."""
import dateutil
import re

# Regular expressions for date time detection
date_regex1 = re.compile(r'(\d+/\d+/\d+)')
date_regex2 = re.compile(r'(\d+-\d+-\d+)')


def is_date(input: str) -> bool:
    """
    Check if a given string is a date.

    Needs regex to make sure the dateutil doesn't allow integers
    interpreted as epochs.

    :param input: Input string to check if it's a date or not
    :return: Whether the given string is a date or not
    """
    if date_regex1.search(input) is None and date_regex2.search(input) is None:
        return False

    try:
        dateutil.parser.parse(input)
        return True
    except ValueError:
        return False
