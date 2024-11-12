import pytest
from openapi_parser.exceptions import ParsingError, ReferenceResolutionError

def test_parsing_error_message():
    try:
        raise ParsingError("Parsing error occurred.")
    except ParsingError as e:
        assert str(e) == "Parsing error occurred."

def test_reference_resolution_error_message():
    try:
        raise ReferenceResolutionError("Reference resolution error.")
    except ReferenceResolutionError as e:
        assert str(e) == "Reference resolution error."
