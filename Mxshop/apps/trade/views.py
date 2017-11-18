# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import redirect
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopingCartSerializer,ShopCartDetailSerializer,OrderInfoSerializer,OrderDetailSerializer
from .models import ShoppingCart,OrderGoods,OrderInfo

# Create your views here.

class ShopCartViewset(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = "goods_id"
    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShopingCartSerializer
    def get_queryset(self):
        queryset = ShoppingCart.objects.filter(user=self.request.user)
        return queryset
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        num = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= num
        goods.save()




class OrderViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderInfoSerializer
    def get_queryset(self):
        queryset = ShoppingCart.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        order = serializer.save()
        #插入OrderGoods表并清空购物车
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order


from rest_framework.views import APIView
from utils.alipay import AliPay
from Mxshop.settings import ali_pub_key_path, private_key_path
from rest_framework.response import Response
#支付宝支付结果通知接口，get:同步，post:异步
class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016080600180695",
            app_notify_url="http://47.92.87.172:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.92.87.172:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    good = order_good.goods
                    good.sold_num += order_good.goods_num
                    good.save()
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("index")
            response.set_cookie("nextPath","pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016080600180695",
            app_notify_url="http://47.92.87.172:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.92.87.172:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")
