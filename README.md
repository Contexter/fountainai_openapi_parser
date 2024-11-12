
# FountainAI OpenAPI Parser

This repository provides a robust OpenAPI parser for the FountainAI ecosystem, enabling efficient parsing and validation of OpenAPI specifications. It's particularly well-suited for integration with FastAPI, allowing developers to validate their OpenAPI specifications programmatically and ensure consistency within API-driven applications.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Integration with FastAPI](#integration-with-fastapi)
- [OpenAPI Parser Components](#openapi-parser-components)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The `fountainai_openapi_parser` is a specialized tool for parsing and validating OpenAPI specifications. When integrated with a FastAPI app, it provides a convenient way to check the accuracy and consistency of OpenAPI documentation used for building RESTful APIs.

## Key Features

- **OpenAPI Parsing**: Parses OpenAPI YAML files into structured data for easy access within FastAPI.
- **Validation**: Ensures OpenAPI specifications adhere to standards.
- **Custom Exceptions**: Provides clear feedback and specific exceptions for handling OpenAPI-related issues.
- **Utility Functions**: Includes helpers for path validation, model checks, and field extraction.
- **Comprehensive Tests**: High test coverage for all parser components, ensuring reliable performance.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Contexter/fountainai_openapi_parser.git
   cd fountainai_openapi_parser
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: This parser requires `PyYAML` specifically for loading YAML files.

## Quick Start

To parse an OpenAPI YAML file, use the `load_openapi_from_file()` function:

```python
from openapi_parser.parser import load_openapi_from_file

spec_path = "openapi_specs/Action-Service.yml"
parsed_spec = load_openapi_from_file(spec_path)
```

To handle any parsing errors:

```python
from openapi_parser.exceptions import ParsingError

try:
    parsed_spec = load_openapi_from_file(spec_path)
except ParsingError as e:
    print("Error parsing OpenAPI spec:", e)
```

You can also parse directly from a YAML string with `load_openapi_from_yaml()`:

```python
from openapi_parser.parser import load_openapi_from_yaml

yaml_content = """
openapi: "3.1.0"
info:
  title: Sample API
  version: "1.0.0"
paths: {}
"""
parsed_spec = load_openapi_from_yaml(yaml_content)
```

## Integration with FastAPI

The parser integrates smoothly into FastAPI, enabling validation of OpenAPI specifications as part of your API's lifecycle. Here’s a step-by-step guide to incorporating the OpenAPI parser in a FastAPI app.

### 1. Parse and Validate OpenAPI Specs on Startup

In FastAPI, you can use a startup event to parse and validate your OpenAPI specs when the application starts. This ensures that all specs are valid before serving any requests.

```python
from fastapi import FastAPI
from openapi_parser.parser import load_openapi_from_file
from openapi_parser.exceptions import ParsingError

app = FastAPI()

@app.on_event("startup")
async def validate_openapi_specs():
    try:
        spec_path = "openapi_specs/Action-Service.yml"
        parsed_spec = load_openapi_from_file(spec_path)
        print("OpenAPI specification loaded successfully")
    except ParsingError as e:
        print(f"Error parsing OpenAPI spec: {e}")
        # Optionally, you could raise an exception to prevent app startup
```

### 2. Access Parsed OpenAPI Data in Endpoints

Once the OpenAPI specification is parsed, you can access it within your endpoints for additional validation or use it to dynamically create responses.

```python
@app.get("/api/paths")
async def list_paths():
    spec_path = "openapi_specs/Action-Service.yml"
    parsed_spec = load_openapi_from_file(spec_path)
    return parsed_spec["paths"]  # Return all paths from the OpenAPI spec
```

### 3. Use OpenAPI Models in FastAPI Endpoints

With the parsed OpenAPI data, you can dynamically use models or schemas from the specification. This is particularly useful for endpoints requiring custom validation based on the OpenAPI file.

```python
from pydantic import BaseModel
from typing import Dict, Any

# Define a model dynamically based on OpenAPI schema
class DynamicModel(BaseModel):
    model_data: Dict[str, Any]

@app.post("/validate")
async def validate_data(data: DynamicModel):
    # Custom validation logic based on parsed OpenAPI spec
    # You could use parsed_spec['components']['schemas'] if your spec has schemas
    return {"status": "validated", "data": data}
```

### 4. Automate OpenAPI Validation in CI/CD Pipeline

To ensure your OpenAPI specifications are always valid, integrate the parser into your CI/CD pipeline. This can be done by running a script that attempts to parse the OpenAPI spec and raises errors if validation fails.

```python
# ci_validate_openapi.py
import sys
from openapi_parser.parser import load_openapi_from_file
from openapi_parser.exceptions import ParsingError

spec_path = "openapi_specs/Action-Service.yml"

try:
    load_openapi_from_file(spec_path)
    print("OpenAPI specification is valid")
except ParsingError as e:
    print(f"OpenAPI specification error: {e}")
    sys.exit(1)  # Exit with an error status if the spec is invalid
```

Add this script as a step in your CI pipeline to automatically validate OpenAPI files.

## OpenAPI Parser Components

The `fountainai_openapi_parser` module is composed of several key components, each essential to parsing and validating OpenAPI specifications:

- **parser.py**: Core parser that reads OpenAPI YAML files, structures data, and ensures format adherence.
- **exceptions.py**: Custom exceptions for handling parsing issues and OpenAPI standard violations.
- **utils.py**: Helper functions to manage paths, validate fields, and facilitate common operations on OpenAPI data.
- **models.py**: Contains internal models for handling structured data, such as schemas and paths, within the OpenAPI spec.

## Testing

Run the provided test suite to verify parser functionality:

```bash
pytest
```

This will execute unit tests covering:
- Parsing and validation functionality.
- Exception handling.
- Utility functions and helper methods.

## Contributing

Contributions are welcome to expand and improve the parser's functionality, add integrations, and enhance test coverage. 

1. Fork this repository.
2. Create a new branch for your changes.
3. Submit a pull request with a clear description of your updates.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This README provides an updated, comprehensive guide for integrating the OpenAPI parser into a FastAPI app, with examples for loading and validating OpenAPI files, using parsed data in endpoints, and automating validation in a CI/CD pipeline.
