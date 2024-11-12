import os
from openapi_parser.exceptions import ReferenceResolutionError

def load_file(path):
    """Loads a file from the given path."""
    # Check if the file exists, and raise OSError if it does not
    if not os.path.exists(path):
        raise OSError(f"File not found: {path}")
    # Open and read the file content
    with open(path, 'r') as f:
        return f.read()

def resolve_references(openapi_instance):
    """Resolves all `$ref` references in the OpenAPI instance.

    Raises:
        ReferenceResolutionError: If a reference cannot be resolved.
    """
    try:
        # Traverse the OpenAPI paths and look for references
        for path, item in openapi_instance.get("paths", {}).items():
            for method, details in item.items():
                responses = details.get("responses", {})
                for code, response in responses.items():
                    content = response.get("content", {})
                    for mime_type, schema in content.items():
                        # Check for an unresolved reference in the schema
                        if "$ref" in schema["schema"]:
                            ref = schema["schema"]["$ref"]
                            ref_path = ref.split('/')[-1]
                            if ref_path not in openapi_instance.get("components", {}).get("schemas", {}):
                                raise ReferenceResolutionError(f"Reference '{ref}' not found.")
                            schema["schema"] = openapi_instance["components"]["schemas"][ref_path]
        return openapi_instance
    except KeyError as e:
        # Raise ReferenceResolutionError if the structure is missing expected keys
        raise ReferenceResolutionError(f"Unresolved reference due to missing key: {e}")
