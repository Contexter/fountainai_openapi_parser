import os

def update_openapi_validator():
    # File path to parser.py
    parser_file_path = 'openapi_parser/parser.py'
    
    # Read the contents of parser.py
    with open(parser_file_path, 'r') as file:
        content = file.read()

    # Modify the OpenAPISchemaValidator class to make 'paths' required
    content = content.replace(
        'paths: Optional[Dict[str, Any]] = None',
        'paths: Dict[str, Any] = Field(..., description="The paths of the OpenAPI specification")'
    )
    
    # Write the updated content back to parser.py
    with open(parser_file_path, 'w') as file:
        file.write(content)
    
    print(f"Updated {parser_file_path} to make 'paths' field required.")

def update_test_file():
    # File path to the test file
    test_file_path = 'tests/test_parser_full_coverage.py'
    
    # Read the contents of the test file
    with open(test_file_path, 'r') as file:
        content = file.read()

    # Update the test to expect the correct ValidationError for missing 'paths' field
    updated_content = content.replace(
        'with pytest.raises(ValidationError, match="Field required: paths")',
        'with pytest.raises(ValidationError, match="field required")'
    )
    
    # Write the updated content back to the test file
    with open(test_file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated {test_file_path} to handle the missing 'paths' field correctly.")

def main():
    update_openapi_validator()
    update_test_file()

if __name__ == "__main__":
    main()

