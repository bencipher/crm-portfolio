from django.urls import path

from search.views import query

urlpatterns = [
    path('', query, name='query'),
]
