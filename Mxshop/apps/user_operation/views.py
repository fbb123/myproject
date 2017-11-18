# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import UserFavSerializer,UserFavDetailSerializer,LeavingMessageSerializer,AddressSerializer
from .models import UserFav,UserLeavingMessage,UserAddress
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.

class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        else:
            return UserFavSerializer
    def get_queryset(self):
        queryset = UserFav.objects.filter(user=self.request.user)
        return queryset
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     instance.save()


class LeavingMessageViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    '''
    list:
        获取用户留言
    create:
        添加留言
    delete"
        删除留言
    '''
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer
    def get_queryset(self):
        queryset = UserLeavingMessage.objects.filter(user=self.request.user)
        return queryset

class AddressViewset(viewsets.ModelViewSet):
    '''
    list:
        获取收货地址
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        queryset = UserAddress.objects.filter(user=self.request.user)
        return queryset
