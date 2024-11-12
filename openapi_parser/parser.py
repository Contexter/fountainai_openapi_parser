import yaml
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from openapi_parser.models import Info, Components
from openapi_parser.exceptions import ParsingError, ReferenceResolutionError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a schema validator for OpenAPI content using Pydantic
class OpenAPISchemaValidator(BaseModel):
    openapi_version: str = Field(..., alias="openapi")
    info: Info
    paths: Dict[str, Any]
    components: Optional[Components] = None
    servers: Optional[list] = []
    tags: Optional[list] = []
    externalDocs: Optional[Any] = None

# Function to parse OpenAPI content from a dictionary
def parse_openapi(content: Dict[str, Any]) -> OpenAPISchemaValidator:
    # Pre-validate required fields before Pydantic schema validation
    if "openapi" not in content:
        raise ParsingError("Invalid OpenAPI specification: Missing 'openapi' field.")
    if content["openapi"] not in ["3.1.0"]:
        raise ParsingError(f"Invalid OpenAPI specification: Unsupported version '{content['openapi']}'.")

    if "info" not in content:
        raise ParsingError("Invalid OpenAPI specification: Missing 'info' field.")
    if "version" not in content["info"]:
        raise ParsingError("Invalid OpenAPI specification: Missing 'version' in 'info' field.")
    if "paths" not in content:
        raise ParsingError("Invalid OpenAPI specification: Missing 'paths' field.")
    
    try:
        # Validate content against OpenAPISchemaValidator
        openapi_instance = OpenAPISchemaValidator.model_validate(content)
        return openapi_instance
    except ValidationError as e:
        raise ParsingError(f"Invalid OpenAPI specification: {e}")
    except Exception as e:
        logger.error("Unexpected error while parsing OpenAPI specification", exc_info=True)
        raise ParsingError(f"Unexpected error while parsing OpenAPI specification: {e}")

# Function to load OpenAPI content from a YAML string
def load_openapi_from_yaml(yaml_content: str) -> OpenAPISchemaValidator:
    try:
        content = yaml.safe_load(yaml_content)
        if not isinstance(content, dict):
            raise ParsingError("YAML content must be a dictionary representing the OpenAPI document.")
        return parse_openapi(content)
    except (yaml.YAMLError, ValidationError) as e:
        raise ParsingError(f"Invalid YAML format: {e}")
    except Exception as e:
        logger.error("Unexpected error while loading OpenAPI from YAML", exc_info=True)
        raise ParsingError(f"Unexpected error while loading OpenAPI from YAML: {e}")

# Function to load OpenAPI content from a file
def load_openapi_from_file(file_path: str) -> OpenAPISchemaValidator:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml_content = file.read()
        return load_openapi_from_yaml(yaml_content)
    except FileNotFoundError as e:
        raise ParsingError(f"File not found: {e}")
    except IOError as e:
        raise ParsingError(f"IO error while reading the file: {e}")
