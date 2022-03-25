import re
from typing import Dict, List, Tuple
from django.conf import settings

from search.enums import ObjectEnum


def get_search_url(object_type: ObjectEnum) -> str:
    return f"https://{settings.ELASTICSEARCH_DSL['default']['host']}/{object_type}/_search"


def get_auth() -> Tuple[str, str]:
    return settings.ELASTICSEARCH_DSL['default']['http_auth']


def _extract_hits(response: Dict, limit: int) -> Dict:
    count = 0
    if "hits" in response:
        hits = [source["_source"] for source in response["hits"]["hits"]]
        count = response['hits']['total']['value']
    else:
        hits = []

    return {
        "start_key": (len(hits) == limit),
        "hits": hits,
        "count": count
    }


def _insert_query(body: Dict, query: str, fields: List[str]) -> Dict:
    alphanums = "()"
    regex = re.compile(alphanums)
    if re.search(regex, query):
        if re.search("[a-zA-Z]", query):
            if '@' in query:
                query = query.replace(".", " ")
            else:
                query = re.sub(f"[{alphanums}]", " ", query)
        else:
            query = re.sub(f"[{alphanums}]", "", query)
    body['query']['bool']['must'].append({
        "simple_query_string": {
            "query": query + "*",
            "fields": fields,
            "default_operator": "and",
            "analyze_wildcard": "true",
            "fuzzy_prefix_length": "15",
            "minimum_should_match": "15<50%"
        }
    })
    return body


def _base_query(size: int, start: int) -> Dict:
    return {
        "size": size,
        "from": start,
        "query": {
            "bool": {
                'filter': [],
                'must': []
            }
        },
        "track_total_hits": True,
    }


def get_object_fields(object_type: ObjectEnum) -> List:
    search_field = {
        'lead': ['assignee.user.first_name', 'assignee.user.last_name', 'assignee.user.email', 'first_name', 'last_name',
                 'email', 'stage', 'source', 'gender', 'marital_status'],
        'agent': ['user.first_name', 'user.last_name', 'user.email']
    }
    return search_field[object_type.value]
