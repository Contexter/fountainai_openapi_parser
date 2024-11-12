import os
import re


# Paths to the files that need to be updated
INFO_MODEL_FILE = 'openapi_parser/models.py'
PARSER_FILE = 'openapi_parser/parser.py'
TEST_FILE = 'tests/test_parser_full_coverage.py'


def update_info_model():
    """Ensure the 'info' model has a required 'version' field."""
    try:
        with open(INFO_MODEL_FILE, 'r') as file:
            content = file.read()

        # Check if 'version' field is already defined as required in the Info model
        if 'class Info(BaseModel):' in content and 'version: str' not in content:
            # Add the 'version' field to the Info model
            new_content = re.sub(r'class Info\(BaseModel\):',
                                 r'class Info(BaseModel):\n    version: str  # Ensure version is required', content)

            with open(INFO_MODEL_FILE, 'w') as file:
                file.write(new_content)
            print(f"Updated {INFO_MODEL_FILE} to ensure 'version' is required in the Info model.")
        else:
            print(f"'version' field already exists in {INFO_MODEL_FILE}. No changes made.")

    except Exception as e:
        print(f"Error while updating {INFO_MODEL_FILE}: {e}")


def update_parser_file():
    """Ensure the 'parse_openapi' function handles the missing 'info.version' field correctly."""
    try:
        with open(PARSER_FILE, 'r') as file:
            content = file.read()

        # Check if the parser function has a validation for missing 'info.version'
        if 'info' in content and 'version' not in content:
            # Update the parser to handle missing info.version
            new_content = re.sub(
                r'(if "info" not in content or "info" not in content):',
                r'if "info" not in content or "info" not in content or "version" not in content["info"]:',
                content)

            with open(PARSER_FILE, 'w') as file:
                file.write(new_content)
            print(f"Updated {PARSER_FILE} to ensure 'info.version' is validated.")
        else:
            print(f"'info.version' validation already exists in {PARSER_FILE}. No changes made.")

    except Exception as e:
        print(f"Error while updating {PARSER_FILE}: {e}")


def update_test_file():
    """Update the test to check if 'info.version' is missing."""
    try:
        with open(TEST_FILE, 'r') as file:
            content = file.read()

        # Check if the test already verifies missing 'info.version'
        if 'test_parse_openapi_incomplete_spec' not in content:
            # Add the test to handle missing 'info.version'
            test_code = """
def test_parse_openapi_incomplete_spec():
    incomplete_spec = {"openapi": "3.1.0", "info": {"title": "Test API"}}
    with pytest.raises(ParsingError, match="Invalid OpenAPI specification: Missing 'info.version' field."):
        parse_openapi(incomplete_spec)
"""
            # Add the test to the end of the file
            new_content = content + test_code

            with open(TEST_FILE, 'w') as file:
                file.write(new_content)
            print(f"Updated {TEST_FILE} to add test for missing 'info.version'.")
        else:
            print(f"Test for missing 'info.version' already exists in {TEST_FILE}. No changes made.")

    except Exception as e:
        print(f"Error while updating {TEST_FILE}: {e}")


def main():
    """Run the updates on the Info model, parser, and test files."""
    update_info_model()
    update_parser_file()
    update_test_file()


if __name__ == "__main__":
    main()

