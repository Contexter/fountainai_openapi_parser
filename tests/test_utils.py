import pytest
from openapi_parser.utils import resolve_references, load_file
from openapi_parser.exceptions import ReferenceResolutionError
import tempfile
import os

# Test for loading an existing file
def test_load_file():
    # Create a temporary file to use in the test
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"sample content")
        temp_file_path = temp_file.name

    try:
        # Load the temporary file and check content
        content = load_file(temp_file_path)
        assert content == "sample content"
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

# Test for unresolved reference in resolve_references
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
