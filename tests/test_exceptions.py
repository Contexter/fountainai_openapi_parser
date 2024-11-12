import pytest
from openapi_parser.exceptions import ParsingError, ReferenceResolutionError

def test_parsing_error():
    with pytest.raises(ParsingError) as exc_info:
        raise ParsingError("Parsing failed")
    assert str(exc_info.value) == "Parsing failed"

def test_reference_resolution_error():
    with pytest.raises(ReferenceResolutionError) as exc_info:
        raise ReferenceResolutionError("Reference resolution failed")
    assert str(exc_info.value) == "Reference resolution failed"
