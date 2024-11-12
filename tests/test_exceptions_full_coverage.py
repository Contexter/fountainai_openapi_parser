import pytest
from openapi_parser.exceptions import ParsingError, ReferenceResolutionError

def test_parsing_error():
    try:
        raise ParsingError("Custom parsing error")
    except ParsingError as e:
        assert str(e) == "Custom parsing error"

def test_reference_resolution_error():
    try:
        raise ReferenceResolutionError("Custom reference resolution error")
    except ReferenceResolutionError as e:
        assert str(e) == "Custom reference resolution error"
