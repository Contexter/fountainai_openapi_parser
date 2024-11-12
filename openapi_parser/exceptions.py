class ParsingError(Exception):
    """
    Raised when an error occurs during parsing of the OpenAPI document.

    Attributes:
        message (str): Description of the parsing error.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(Exception):
    """
    Raised when the OpenAPI document fails validation.

    Attributes:
        message (str): Description of the validation error.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ReferenceResolutionError(Exception):
    """
    Raised when there is an issue resolving $ref references in the OpenAPI
    document.

    Attributes:
        message (str): Description of the reference resolution error.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
