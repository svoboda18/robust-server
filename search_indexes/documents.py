from django_elasticsearch_dsl import Document, fields

from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer

from startup.models import Startup

html_strip = analyzer(
    'html_strip',
    tokenizer="whitespace",
    filter=["lowercase"],
    char_filter=["html_strip"]
)

@registry.register_document
class StartupDocument(Document):
    id = fields.IntegerField(attr='id')
    investors = fields.TextField(
        attr='investors_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )
    name = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    category = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )

    class Index:
        name = 'startup'

    class Django:
        model = Startup
        fields = [
    'status',
    'description',
    'start_date',
    'website',
    'industry',
    'founder',
    'headquarters',
    'funding_amount',
    'created_at',
    'updated_at'
        ]