from typing import Any, List, Optional
from django.db import models
from pydantic import BaseModel
from search.enums import FieldEnum, ObjectEnum, OperatorEnum, SortOrder


# Create your models here.


class FilterModel(BaseModel):
    """Query filter model used for filtering search results"""
    path: FieldEnum
    value: Optional[Any]
    operator: OperatorEnum = OperatorEnum.equal


class ElasticSearchRequest(BaseModel):
    query: Optional[str]
    object_type: ObjectEnum
    start_hits: int = 0
    page_size: int = 50
