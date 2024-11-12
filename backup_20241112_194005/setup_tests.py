import os
from pathlib import Path
import subprocess

# Define test file content templates
test_parser_content = """\
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
"""

test_exceptions_content = """\
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
"""

test_utils_content = """\
import pytest
from openapi_parser.utils import resolve_references, load_file
from openapi_parser.exceptions import ReferenceResolutionError

def test_load_file():
    content = load_file("sample_path_or_content")
    assert content == "sample_path_or_content"

def test_resolve_references():
    openapi_instance = {
        "components": {
            "schemas": {
                "Example": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"}
                    }
                }
            }
        },
        "paths": {
            "/test": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Example"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    result = resolve_references(openapi_instance)
    assert result["paths"]["/test"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["properties"]["id"]["type"] == "string"
"""

# Define the directory structure
test_directory = Path("tests")
test_directory.mkdir(exist_ok=True)

# Write test files
(test_directory / "test_parser.py").write_text(test_parser_content)
(test_directory / "test_exceptions.py").write_text(test_exceptions_content)
(test_directory / "test_utils.py").write_text(test_utils_content)

# Install required packages
print("Installing pytest and pytest-cov...")
subprocess.run(["pip", "install", "pytest", "pytest-cov"])

# Explicitly set PYTHONPATH for pytest to recognize openapi_parser
os.environ["PYTHONPATH"] = os.path.abspath(".")

# Run tests with coverage
print("Running tests with coverage...")
subprocess.run(["pytest", "--cov=openapi_parser", "tests/"])

print("Setup complete! All tests have been created and executed with coverage.")
