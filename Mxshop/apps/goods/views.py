# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods,GoodsCategory,Banner
from .serializers import GoodsSerializer,GoodsCategorySerializer,BannerSerializer,IndexCategorySerializer
from .filters import GoodsFilter

# Create your views here.

#定制化分页
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class CategoryViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer

class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().order_by("index")

class IndexCategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = IndexCategorySerializer
    queryset = GoodsCategory.objects.filter(is_tab=True)