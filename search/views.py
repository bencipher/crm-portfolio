import requests
from rest_framework.decorators import api_view
from libs.aws.es import _base_query, _extract_hits, _insert_query, get_auth, get_object_fields, get_search_url
from search.models import ElasticSearchRequest
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def query(request):
    data = ElasticSearchRequest(**request.data)
    body = _base_query(data.page_size, data.start_hits)
    object_type = data.object_type
    search_url = get_search_url(object_type)
    if data.query:
        query_field = get_object_fields(object_type)
        body = _insert_query(body, data.query, query_field)
    # FILTERS
    # todo implement filters for indices
    try:
        r = requests.get(search_url, auth=get_auth(), json=body, headers={"Content-Type": "application/json"}).json()
    except Exception as e:
        raise Exception(str(e))
    return Response({'data': _extract_hits(r, len(r['hits']['hits']))}, status=status.HTTP_200_OK)
