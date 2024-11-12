# openapi_schema_validator.py
from pydantic import BaseModel
from typing import Dict, Optional
from .models import Info, PathItem, Components, Tag, ExternalDocumentation

class OpenAPISchemaValidator(BaseModel):
    openapi: str
    info: Info
    paths: Dict[str, PathItem]
    components: Optional[Components] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    tags: Optional[List[Tag]] = None
    externalDocs: Optional[ExternalDocumentation] = None

    class Config:
        orm_mode = True

