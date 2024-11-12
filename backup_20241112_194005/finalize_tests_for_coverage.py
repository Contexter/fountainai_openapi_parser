import os
from pathlib import Path
import subprocess

# Additional test content to ensure full coverage

# Tests for exceptions.py
test_exceptions_full_coverage_content = """\
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
"""

# Tests for parser.py
test_parser_full_coverage_content = """\
import pytest
from openapi_parser.parser import parse_openapi, load_openapi_from_yaml, load_openapi_from_file
from openapi_parser.exceptions import ParsingError
from pydantic import ValidationError

# Test missing 'info' key in OpenAPI content
def test_parse_openapi_missing_info():
    content = {"openapi": "3.1.0"}
    with pytest.raises(ParsingError, match="Missing 'openapi' or 'info' fields."):
        parse_openapi(content)

# Test parsing with incomplete OpenAPI spec (line 35 in parser.py)
def test_parse_openapi_incomplete_spec():
    incomplete_spec = {"openapi": "3.1.0", "info": {"title": "Test API"}}
    with pytest.raises(ValidationError, match="Field required: paths"):
        parse_openapi(incomplete_spec)

# Test parsing file that does not exist (line 74 in parser.py)
def test_load_openapi_from_file_not_found():
    with pytest.raises(ParsingError, match="File not found"):
        load_openapi_from_file("non_existent_file.yaml")
"""

# Tests for utils.py (covering line 37 for unresolved references)
test_utils_full_coverage_content = """\
import pytest
from openapi_parser.utils import resolve_references
from openapi_parser.exceptions import ReferenceResolutionError

def test_resolve_references_invalid_ref():
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
        },
        "components": {
            "schemas": {
                "ExistingSchema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"}
                    }
                }
            }
        }
    }
    with pytest.raises(ReferenceResolutionError, match="Reference '#/components/schemas/Nonexistent' not found"):
        resolve_references(openapi_instance)
"""

# Define the path for the new test files
test_directory = Path("tests")
test_directory.mkdir(exist_ok=True)

# Write the new test files to extend coverage
(test_directory / "test_exceptions_full_coverage.py").write_text(test_exceptions_full_coverage_content)
(test_directory / "test_parser_full_coverage.py").write_text(test_parser_full_coverage_content)
(test_directory / "test_utils_full_coverage.py").write_text(test_utils_full_coverage_content)

# Set PYTHONPATH to ensure all modules are accessible for pytest
os.environ["PYTHONPATH"] = os.path.abspath(".")

# Run all tests with coverage to check if we achieve 100%
print("Running all tests with coverage...")
subprocess.run(["pytest", "--cov=openapi_parser", "--cov-report=term-missing", "tests/"])

print("Final tests for full coverage setup complete! All additional tests have been created and executed.")

