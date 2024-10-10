from fastapi import APIRouter, Header, Depends

from pydantic.main import BaseModel

from api import ok, mysql

router = APIRouter()
