import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import GoodsDocument

class GoodsDocumentSerializer(DocumentSerializer):
    """Serializer for the Book document."""

    name = serializers.CharField(read_only=True,fielddata=True)
    class Meta(object):
        """Meta options."""

        # Specify the correspondent document class
        document = GoodsDocument

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            'id'
            'name',
            'goods_sn',
            'market_price',
            'shop_price',
            'click_num',
            'sold_num',
            'fav_num',
            'goods_num',
        )