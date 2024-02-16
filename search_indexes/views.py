from .documents import StartupDocument
from .serializers import StartupDocumentSerializer

from elasticsearch_dsl import DateHistogramFacet

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_CONTAINS,
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
    FacetedSearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

class StartupViewSet(DocumentViewSet):
    serializer_class = StartupDocumentSerializer

    document = StartupDocument
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FacetedSearchFilterBackend,
        SuggesterFilterBackend
    ]
    search_fields = (
        'name',
        'category',
        'investors',
        'founder',
        'website'
    )

    suggester_fields = {
        'name_suggest': {
            'field': 'name.suggest',
            'suggesters': [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 7,
                'skip_duplicates': True,
            },
        },
    }
    filter_fields = {
        'date': {
            'field': 'created_at',
            'lookups': [
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_LTE,
                LOOKUP_QUERY_LT,
            ],
        },
        'category.raw': {
            'field': 'category.raw',
            'lookups': [
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
            ],
        },
        'category': {
            'field': 'category',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_CONTAINS
            ],
        },
    }
    faceted_search_fields = {
        'date': {
            'field': 'created_at',
            'facet': DateHistogramFacet,
            'enabled': True,
            'options': {
                'fixed_interval': '1d',
            },
        },
    }
    
    ordering_fields = {
        'date': 'created_at',
    }
    ordering = ('-date',)
