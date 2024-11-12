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
