from rest_framework import serializers
from django.db.models import Q
from .models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd


class GoodsCategorySerializer3(serializers.ModelSerializer):
    '''
    获取三级类目
    '''

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer2(serializers.ModelSerializer):
    '''
    获取二级类目
    '''
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer(serializers.ModelSerializer):
    '''
    获取一级类目
    '''
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BannerSerializer(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            ad_goods_serializer = GoodsSerializer(goods_ins, many=False,context={"request":self.context["request"]})
            return ad_goods_serializer.data
        else:
            return None

    goods = serializers.SerializerMethodField()

    # 这里不能用goods = GoodsSerializer(many=True)获取goods，因为商品的直接所属类目可能不是一级类目
    def get_goods(self, obj):
        goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(goods, many=True,context={"request":self.context["request"]})
        return goods_serializer.data

    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"
