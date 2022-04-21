from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch


def bulk_indexing():
    BlogPostIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.BlogPost.objects.all().iterator()))


