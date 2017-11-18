import django_filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    price_min = django_filters.NumberFilter(name='shop_price',lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='shop_price',lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='get_category_filter')

    def get_category_filter(self,queryset,name,value):
        queryset = queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))
        return queryset
    class Meta:
        model = Goods
        fields = ['price_min','price_max','is_hot','is_new']
