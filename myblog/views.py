# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics

from .models import Category,Tag,Post
from .serializers import CategorySerializer,TagSerializer,PostSerializer
# Create your views here.
class Post_lc(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
class Post_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
