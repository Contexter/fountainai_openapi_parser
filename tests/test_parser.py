import pytest
from openapi_parser.parser import parse_openapi, load_openapi_from_yaml, load_openapi_from_file
from openapi_parser.exceptions import ParsingError

# Sample OpenAPI content for testing
valid_openapi_content = {
    "openapi": "3.1.0",
    "info": {
        "title": "Test API",
        "version": "1.0.0"
    },
    "paths": {}
}

invalid_openapi_content = {
    # 'openapi' field is missing to simulate an invalid specification
    "info": {
        "title": "Test API",
        "version": "1.0.0"
    }
}

def test_parse_openapi_success():
    result = parse_openapi(valid_openapi_content)
    assert result.info.title == "Test API"  # Use dot notation for Pydantic model fields

def test_parse_openapi_failure():
    with pytest.raises(ParsingError):
        parse_openapi(invalid_openapi_content)

def test_load_openapi_from_yaml_success():
    yaml_content = '''
    openapi: "3.1.0"
    info:
      title: "Test API"
      version: "1.0.0"
    paths: {}
    '''
    result = load_openapi_from_yaml(yaml_content)
    assert result.info.title == "Test API"  # Use dot notation

def test_load_openapi_from_yaml_failure():
    invalid_yaml = '''
    info:
      title: "Test API"
      version: "1.0.0"
    '''
    with pytest.raises(ParsingError):
        load_openapi_from_yaml(invalid_yaml)

def test_load_openapi_from_file(tmp_path):
    valid_file = tmp_path / "valid_openapi.yaml"
    valid_file.write_text('''
    openapi: "3.1.0"
    info:
      title: "Test API"
      version: "1.0.0"
    paths: {}
    ''')
    result = load_openapi_from_file(str(valid_file))
    assert result.info.title == "Test API"  # Use dot notation

    invalid_file = tmp_path / "invalid_openapi.yaml"
    invalid_file.write_text('''
    info:
      title: "Test API"
      version: "1.0.0"
    ''')
    with pytest.raises(ParsingError):
        load_openapi_from_file(str(invalid_file))
