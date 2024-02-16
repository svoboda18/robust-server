from rest_framework.serializers import SerializerMethodField
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import StartupDocument

class StartupDocumentSerializer(DocumentSerializer):
    investors = SerializerMethodField()

    class Meta:
        document = StartupDocument

    def get_investors(self, obj):
        """Get Investors."""
        if obj.investors:
            return list(obj.investors)
        else:
            return []