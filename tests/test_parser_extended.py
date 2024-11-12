import pytest
from openapi_parser import parse_openapi
from openapi_parser.exceptions import ParsingError


def test_parse_openapi_success():
    valid_openapi_content = {
        "openapi": "3.1.0",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {}
    }
    openapi_instance = parse_openapi(valid_openapi_content)
    assert openapi_instance.openapi_version == "3.1.0"
    assert openapi_instance.info.title == "Test API"
    assert openapi_instance.info.version == "1.0.0"
    assert openapi_instance.paths == {}


def test_parse_openapi_failure():
    invalid_openapi_content = {
        "openapi": "3.1.0",
        "info": {"title": "Test API"}  # Missing 'version' and 'paths'
    }
    try:
        parse_openapi(invalid_openapi_content)
    except ParsingError as e:
        error_message = str(e)
        assert "Invalid OpenAPI specification" in error_message
        assert "Missing 'version' in 'info' field" in error_message
    else:
        pytest.fail("Expected ParsingError was not raised.")


def test_missing_info():
    invalid_openapi_content = {
        "openapi": "3.1.0",
        "paths": {}
    }
    try:
        parse_openapi(invalid_openapi_content)
    except ParsingError as e:
        error_message = str(e)
        assert "Invalid OpenAPI specification: Missing 'info' field" in error_message
    else:
        pytest.fail("Expected ParsingError was not raised.")


def test_missing_paths():
    invalid_openapi_content = {
        "openapi": "3.1.0",
        "info": {"title": "Test API", "version": "1.0.0"}
    }
    try:
        parse_openapi(invalid_openapi_content)
    except ParsingError as e:
        error_message = str(e)
        assert "Invalid OpenAPI specification: Missing 'paths' field" in error_message
    else:
        pytest.fail("Expected ParsingError was not raised.")


def test_incorrect_field_type():
    invalid_openapi_content = {
        "openapi": "3.1.0",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": "incorrect_value"  # Should be a dictionary, not a string
    }
    try:
        parse_openapi(invalid_openapi_content)
    except ParsingError as e:
        error_message = str(e)
        assert "Invalid OpenAPI specification" in error_message
        assert "paths" in error_message
    else:
        pytest.fail("Expected ParsingError was not raised.")


def test_invalid_version():
    invalid_openapi_content = {
        "openapi": "3.0.0",  # Invalid version for this test
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {}
    }
    try:
        parse_openapi(invalid_openapi_content)
    except ParsingError as e:
        error_message = str(e)
        assert "Invalid OpenAPI specification: Unsupported version '3.0.0'" in error_message
    else:
        pytest.fail("Expected ParsingError was not raised.")
