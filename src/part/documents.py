from django_elasticsearch_dsl import Index, fields
from django_elasticsearch_dsl.documents import DocType

from part.models import Stock

PART_INDEX_NAME = "part"
part = Index(PART_INDEX_NAME)


@part.doc_type
class StockDocument(DocType):
    part = fields.ObjectField(
        properties={
            "reference": fields.TextField(),
        }
    )

    class Django:
        model = Stock
        fields = ["title"]
