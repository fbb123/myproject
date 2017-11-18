from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer
from goods.models import Goods

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
)


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class GoodsDocument(DocType):
    """Goods Elasticsearch document."""
    id = fields.IntegerField(attr='id')

    name = fields.StringField(
        analyzer=html_strip,
        fields={
                'raw': fields.StringField(analyzer='keyword'),
            },
        )




    goods_sn = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )



    market_price = fields.FloatField()
    shop_price = fields.FloatField()

    click_num = fields.IntegerField()

    sold_num = fields.IntegerField()
    fav_num = fields.IntegerField()
    goods_num = fields.IntegerField()


    class Meta(object):
        """Meta options."""

        model = Goods  # The model associate with this DocType