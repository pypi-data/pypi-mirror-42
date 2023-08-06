from pydantic import BaseModel, Schema
from typing import List, Dict, Optional, Tuple
from enum import Enum


class YamlInput(BaseModel):
    filename: str


class HttpInputMethod(Enum):
    GET = "get"
    POST = "post"
    UPDATE = "update"
    DELETE = "delete"


class HttpInput(BaseModel):
    url: str
    method: HttpInputMethod
    headers: Optional[Dict[str, str]]


class Connection(BaseModel):
    hostname: str
    username: Optional[str]
    password: Optional[str]
    private_key: Optional[str]


class Transform(BaseModel):
    filename: str
    sources: Optional[str]
    destination: str
    connection: Optional[str]


class Document(BaseModel):
    connection: Optional[Dict[str, Connection]]
    transform: Optional[Dict[str, Transform]]
    yaml: Optional[Dict[str, YamlInput]]
    http: Optional[Dict[str, HttpInput]]
