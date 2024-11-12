# openapi_parser/models.py
from enum import Enum
from pydantic import BaseModel, Field, AnyUrl, EmailStr, RootModel
from typing import Optional, List, Dict, Union, Any
from pydantic.class_validators import root_validator


# Define Enums for fields that use predefined values
class ParameterLocation(str, Enum):
    QUERY = "query"
    HEADER = "header"
    PATH = "path"
    COOKIE = "cookie"


class Style(str, Enum):
    MATRIX = "matrix"
    LABEL = "label"
    FORM = "form"
    SIMPLE = "simple"
    SPACE_DELIMITED = "spaceDelimited"
    PIPE_DELIMITED = "pipeDelimited"
    DEEP_OBJECT = "deepObject"


class SecuritySchemeType(str, Enum):
    API_KEY = "apiKey"
    HTTP = "http"
    MUTUAL_TLS = "mutualTLS"
    OAUTH2 = "oauth2"
    OPENID_CONNECT = "openIdConnect"


# Contact information for the exposed API
class Contact(BaseModel):
    name: Optional[str] = None
    url: Optional[AnyUrl] = None
    email: Optional[EmailStr] = None


# License information for the exposed API
class License(BaseModel):
    name: str
    identifier: Optional[str] = None
    url: Optional[AnyUrl] = None


# General information about the API
class Info(BaseModel):
    title: str
    description: Optional[str] = None
    termsOfService: Optional[AnyUrl] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None
    version: str


# Variable substitutions for server URL template
class ServerVariable(BaseModel):
    enum: Optional[List[str]] = None
    default: str
    description: Optional[str] = None


# An object representing a Server
class Server(BaseModel):
    url: str
    description: Optional[str] = None
    variables: Optional[Dict[str, ServerVariable]] = None


# Additional external documentation
class ExternalDocumentation(BaseModel):
    description: Optional[str] = None
    url: AnyUrl


# Allows adding meta-data to a single tag
class Tag(BaseModel):
    name: str
    description: Optional[str] = None
    externalDocs: Optional["ExternalDocumentation"] = None  # Forward reference


# A simple object to allow referencing other components
class Reference(BaseModel):
    ref: str = Field(..., alias="$ref")
    summary: Optional[str] = None
    description: Optional[str] = None


class Config:
    populate_by_name = True


# A metadata object that allows for more fine-tuned XML model definitions
class XML(BaseModel):
    name: Optional[str] = None
    namespace: Optional[AnyUrl] = None
    prefix: Optional[str] = None
    attribute: Optional[bool] = None
    wrapped: Optional[bool] = None


# Adds support for polymorphism and inheritance
class Discriminator(BaseModel):
    propertyName: str
    mapping: Optional[Dict[str, str]] = None


# A single encoding definition applied to a single schema property
class Encoding(BaseModel):
    contentType: Optional[str] = None
    headers: Optional[Dict[str, Union["Header", Reference]]] = None
    style: Optional[Style] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None


# An example of the media type
class Example(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    value: Optional[Any] = None
    externalValue: Optional[AnyUrl] = None


# Each Media Type object provides schema and examples for the media type identified by its key
class MediaType(BaseModel):
    schema_data: Optional[Union["Schema", Reference]] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    encoding: Optional[Dict[str, Encoding]] = None


# The Schema Object allows the definition of input and output data types
class Schema(BaseModel):
    ref: Optional[str] = Field(default=None, alias="$ref")

    # Metadata
    title: Optional[str] = None
    description: Optional[str] = None
    default: Optional[Any] = None
    deprecated: Optional[bool] = None

    readOnly: Optional[bool] = None
    writeOnly: Optional[bool] = None
    examples: Optional[List[Any]] = None

    # String-specific properties
    type: Optional[Union[str, List[str]]] = None
    format: Optional[str] = None
    maxLength: Optional[int] = None
    minLength: Optional[int] = None
    pattern: Optional[str] = None
    contentMediaType: Optional[str] = None
    contentEncoding: Optional[str] = None
    contentSchema: Optional["Schema"] = None

    # Number-specific properties
    multipleOf: Optional[float] = None
    maximum: Optional[float] = None
    exclusiveMaximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusiveMinimum: Optional[float] = None

    # Array-specific properties
    items: Optional[Union["Schema", List["Schema"]]] = None
    prefixItems: Optional[List["Schema"]] = None
    contains: Optional["Schema"] = None
    maxItems: Optional[int] = None
    minItems: Optional[int] = None
    uniqueItems: Optional[bool] = None
    maxContains: Optional[int] = None
    minContains: Optional[int] = None
    unevaluatedItems: Optional[Union["Schema", bool]] = None

    # Object-specific properties
    properties: Optional[Dict[str, "Schema"]] = None
    patternProperties: Optional[Dict[str, "Schema"]] = None
    additionalProperties: Optional[Union["Schema", bool]] = None
    maxProperties: Optional[int] = None
    minProperties: Optional[int] = None
    required: Optional[List[str]] = None
    dependentRequired: Optional[Dict[str, List[str]]] = None
    dependentSchemas: Optional[Dict[str, "Schema"]] = None
    propertyNames: Optional["Schema"] = None
    unevaluatedProperties: Optional[Union["Schema", bool]] = None

    # Conditional and logical keywords
    allOf: Optional[List["Schema"]] = None
    anyOf: Optional[List["Schema"]] = None
    oneOf: Optional[List["Schema"]] = None
    not_: Optional["Schema"] = Field(default=None, alias="not")
    if_: Optional["Schema"] = Field(default=None, alias="if")
    then: Optional["Schema"] = None
    else_: Optional["Schema"] = Field(default=None, alias="else")

    # Enumeration and constant values
    enum: Optional[List[Any]] = None
    const: Optional[Any] = None

    # Discriminator for polymorphism
    discriminator: Optional[Discriminator] = None

    # XML model definitions
    xml: Optional[XML] = None

    # External documentation
    externalDocs: Optional[ExternalDocumentation] = None

    # Example value
    example: Optional[Any] = None

    class Config:
        populate_by_name = True


# Describes a single operation parameter
class Parameter(BaseModel):
    name: str
    in_: ParameterLocation = Field(..., alias="in")
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    allowEmptyValue: Optional[bool] = None
    style: Optional[Style] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None
    schema_data: Optional[Union[Schema, Reference]] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    content: Optional[Dict[str, MediaType]] = None

    class Config:
        populate_by_name = True


# Describes a single request body
class RequestBody(BaseModel):
    description: Optional[str] = None
    content: Dict[str, MediaType]
    required: Optional[bool] = None


# Describes a single response from an API Operation
class Response(BaseModel):
    description: str
    headers: Optional[Dict[str, Union["Header", Reference]]] = None
    content: Optional[Dict[str, MediaType]] = None
    links: Optional[Dict[str, Union["Link", Reference]]] = None


# The Link object represents a possible design-time link for a response
class Link(BaseModel):
    operationRef: Optional[str] = None
    operationId: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    requestBody: Optional[Any] = None
    description: Optional[str] = None
    server: Optional[Server] = None


# Header follows the structure of the Parameter Object with some changes
class Header(BaseModel):
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    allowEmptyValue: Optional[bool] = None
    style: Optional[Style] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None
    schema_data: Optional[Union[Schema, Reference]] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    content: Optional[Dict[str, MediaType]] = None


# A map of possible out-of-band callbacks related to the parent operation
class Callback(RootModel[Dict[str, Union["PathItem", Reference]]]):
    pass


# Defines a security scheme that can be used by the operations
class SecurityScheme(BaseModel):
    type: SecuritySchemeType
    description: Optional[str] = None
    name: Optional[str] = None
    in_: Optional[ParameterLocation] = Field(default=None, alias="in")
    scheme: Optional[str] = None
    bearerFormat: Optional[str] = None
    flows: Optional["OAuthFlows"] = None
    openIdConnectUrl: Optional[AnyUrl] = None

    class Config:
        populate_by_name = True


# Allows configuration of the supported OAuth Flows
class OAuthFlows(BaseModel):
    implicit: Optional["OAuthFlow"] = None
    password: Optional["OAuthFlow"] = None
    clientCredentials: Optional["OAuthFlow"] = None
    authorizationCode: Optional["OAuthFlow"] = None


# Configuration details for a supported OAuth Flow
class OAuthFlow(BaseModel):
    authorizationUrl: Optional[AnyUrl] = None
    tokenUrl: Optional[AnyUrl] = None
    refreshUrl: Optional[AnyUrl] = None
    scopes: Dict[str, str]


# Describes a single API operation on a path
class Operation(BaseModel):
    tags: Optional[List[str]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocumentation] = None
    operationId: Optional[str] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None
    requestBody: Optional[Union[RequestBody, Reference]] = None
    responses: Dict[str, Union[Response, Reference]]
    callbacks: Optional[Dict[str, Union[Callback, Reference]]] = None
    deprecated: Optional[bool] = None
    security: Optional[List[Dict[str, List[str]]]] = None  # SecurityRequirements
    servers: Optional[List[Server]] = None


# Describes the operations available on a single path
class PathItem(BaseModel):
    ref: Optional[str] = Field(default=None, alias="$ref")
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    trace: Optional[Operation] = None
    servers: Optional[List[Server]] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None

    class Config:
        populate_by_name = True


# Holds a set of reusable objects for different aspects of the OAS
class Components(BaseModel):
    schemas: Optional[Dict[str, Union[Schema, Reference]]] = None
    responses: Optional[Dict[str, Union[Response, Reference]]] = None
    parameters: Optional[Dict[str, Union[Parameter, Reference]]] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    requestBodies: Optional[Dict[str, Union[RequestBody, Reference]]] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    securitySchemes: Optional[Dict[str, Union[SecurityScheme, Reference]]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None
    callbacks: Optional[Dict[str, Union[Callback, Reference]]] = None
    pathItems: Optional[Dict[str, Union[PathItem, Reference]]] = None


# The root document object of the OpenAPI document
class OpenAPI(BaseModel):
    openapi: str
    info: Info
    jsonSchemaDialect: Optional[AnyUrl] = None
    servers: Optional[List[Server]] = None
    paths: dict
    webhooks: Optional[Dict[str, Union[PathItem, Reference]]] = None
    components: Optional[Components] = None
    security: Optional[List[Dict[str, List[str]]]] = None  # SecurityRequirements
    tags: Optional[List[Tag]] = None
    externalDocs: Optional[ExternalDocumentation] = None


# Rebuild models to update forward references
Contact.model_rebuild()
License.model_rebuild()
Info.model_rebuild()
ServerVariable.model_rebuild()
Server.model_rebuild()
ExternalDocumentation.model_rebuild()
Tag.model_rebuild()
Reference.model_rebuild()
XML.model_rebuild()
Discriminator.model_rebuild()
Encoding.model_rebuild()
Example.model_rebuild()
MediaType.model_rebuild()
Schema.model_rebuild()
Parameter.model_rebuild()
RequestBody.model_rebuild()
Response.model_rebuild()
Link.model_rebuild()
Header.model_rebuild()
Callback.model_rebuild()
SecurityScheme.model_rebuild()
OAuthFlows.model_rebuild()
OAuthFlow.model_rebuild()
Operation.model_rebuild()
PathItem.model_rebuild()
Components.model_rebuild()
OpenAPI.model_rebuild()

# --- Append the OpenAPISchemaValidator class here ---

# openapi_parser/models.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional, List
from .models import Info, PathItem, Components, Tag, ExternalDocumentation

class OpenAPISchemaValidator(BaseModel):
    openapi_version: str = Field(alias='openapi')
    info: Info
    paths: Dict[str, PathItem]
    components: Optional[Components] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    tags: Optional[List[Tag]] = None
    externalDocs: Optional[ExternalDocumentation] = None

    model_config = ConfigDict(
        populate_by_name=True,  # Ensures that aliases are respected
        from_attributes=True
    )
