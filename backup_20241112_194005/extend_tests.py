import os
from pathlib import Path
import subprocess

# Define additional test file content to improve coverage

# Tests for exceptions
test_exceptions_extended_content = """\
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
"""

# Additional tests for parser.py, especially for error handling
test_parser_extended_content = """\
import pytest
from openapi_parser.parser import parse_openapi, load_openapi_from_yaml, load_openapi_from_file
from openapi_parser.exceptions import ParsingError
from pydantic import ValidationError

# Test missing 'info' key in OpenAPI content
def test_parse_openapi_missing_info():
    content = {"openapi": "3.1.0"}
    with pytest.raises(ParsingError, match="Missing 'openapi' or 'info' fields."):
        parse_openapi(content)

# Test non-dictionary input in load_openapi_from_yaml
def test_load_openapi_from_yaml_invalid_type():
    yaml_content = "- just\\n- a list\\n- not a dict"
    with pytest.raises(ParsingError, match="YAML content must be a dictionary"):
        load_openapi_from_yaml(yaml_content)

# Test invalid YAML content in load_openapi_from_yaml
def test_load_openapi_from_yaml_parse_error():
    invalid_yaml = 'invalid: [unclosed, list'
    with pytest.raises(ParsingError, match="Invalid OpenAPI document structure"):
        load_openapi_from_yaml(invalid_yaml)

# Test file not found error in load_openapi_from_file
def test_load_openapi_from_file_not_found():
    with pytest.raises(ParsingError, match="File not found"):
        load_openapi_from_file("nonexistent_file.yaml")
"""

# Additional tests for untested functions in utils.py
test_utils_extended_content = """\
import pytest
from openapi_parser.utils import resolve_references, load_file
from openapi_parser.exceptions import ReferenceResolutionError

# Test for missing file in load_file
def test_load_file_missing_file():
    with pytest.raises(OSError, match="File not found"):
        load_file("nonexistent_file.txt")

# Test for unresolved reference in resolve_references
def test_resolve_references_missing_ref():
    openapi_instance = {
        "paths": {
            "/test": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Nonexistent"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    with pytest.raises(ReferenceResolutionError, match="Reference '#/components/schemas/Nonexistent' not found"):
        resolve_references(openapi_instance)
"""

# Define paths and create the test files
test_directory = Path("tests")
test_directory.mkdir(exist_ok=True)

# Write the new test files for extended coverage
(test_directory / "test_exceptions_extended.py").write_text(test_exceptions_extended_content)
(test_directory / "test_parser_extended.py").write_text(test_parser_extended_content)
(test_directory / "test_utils_extended.py").write_text(test_utils_extended_content)

# Set PYTHONPATH to ensure all modules are accessible for pytest
os.environ["PYTHONPATH"] = os.path.abspath(".")

# Run the extended tests with coverage
print("Running extended tests with coverage...")
subprocess.run(["pytest", "--cov=openapi_parser", "--cov-report=term-missing", "tests/"])

print("Extended tests setup complete! All additional tests have been created and executed.")
