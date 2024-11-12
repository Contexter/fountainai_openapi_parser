import logging
from .parser import parse_openapi
from .exceptions import ParsingError, ValidationError, ReferenceResolutionError

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

__all__ = [
    "parse_openapi",
    "ParsingError",
    "ValidationError",
    "ReferenceResolutionError",
]

# Example usage of the logger within the package
logger.info("FountainAI OpenAPI Parser package initialized.")
