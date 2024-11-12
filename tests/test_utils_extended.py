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
