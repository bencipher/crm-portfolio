from typing import Any, Dict, List, Optional
from utilities.enums import StrEnum


class ObjectEnum(StrEnum):
    lead = 'lead'
    agent = 'agent'


class SortOrder(StrEnum):
    ascending = "asc"
    descending = "desc"


class OperatorEnum(StrEnum):
    equal = '=='
    exists = '?'
    gte = '>='
    lte = '<='
    lt = '<'
    gt = '>'


class FieldEnum(StrEnum):
    gender = 'gender'
    marital_status = 'marital_status'
    source = 'source'
    stage = 'stage'
    date_created = 'date_created'
    date_updated = 'date_updated'
    assignee = 'assignee'
    first_name = 'first_name'
    last_name = 'last_name'
    email = 'email'
    is_customer = 'is_customer'
    user = 'user'
    is_superuser = 'is_superuser'
