import os
from pathlib import Path
import subprocess

# Define additional test file content to cover the missing lines

# This additional test will cover the unresolved reference case in resolve_references (line 37 in utils.py)
test_utils_additional_content = """\
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

    # This should raise a ReferenceResolutionError because "Nonexistent" is not in components/schemas
    with pytest.raises(ReferenceResolutionError, match="Reference '#/components/schemas/Nonexistent' not found."):
        resolve_references(openapi_instance)
"""

# Define the path for the new test file
test_directory = Path("tests")
test_directory.mkdir(exist_ok=True)

# Write the new test file to extend coverage
(test_directory / "test_utils_additional.py").write_text(test_utils_additional_content)

# Set PYTHONPATH to ensure all modules are accessible for pytest
os.environ["PYTHONPATH"] = os.path.abspath(".")

# Run all tests with coverage to check if we achieved 100%
print("Running all tests with coverage...")
subprocess.run(["pytest", "--cov=openapi_parser", "--cov-report=term-missing", "tests/"])

print("Extended tests for coverage setup complete! All additional tests have been created and executed.")

