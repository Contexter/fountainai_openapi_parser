import os
import yaml
from openapi_parser.parser import parse_openapi  # Ensure this import matches your setup

# Directory containing the OpenAPI specifications
openapi_dir = 'openapi_specs'

# Iterate over each OpenAPI file in the directory
for filename in os.listdir(openapi_dir):
    if filename.endswith('.yml') or filename.endswith('.yaml'):
        file_path = os.path.join(openapi_dir, filename)
        print(f"Testing {filename}")

        try:
            # Load YAML content
            with open(file_path, 'r') as file:
                openapi_content = yaml.safe_load(file)

            # Parse OpenAPI content
            parsed_spec = parse_openapi(openapi_content)
            print(f"{filename} parsed successfully.")
        except Exception as e:
            print(f"Failed to parse {filename}: {e}")

