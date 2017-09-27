# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=100,verbose_name=u'标签')
    created = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    class Meta:
        verbose_name=u'文章标签'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name=u'分类')
    created = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    class Meta:
        verbose_name=u'文章分类'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name
class Post(models.Model):
    category = models.ForeignKey(Category,verbose_name=u'文章分类')
    title = models.CharField(max_length=100,verbose_name=u'文章标题')
    content = models.TextField(verbose_name=u'文章内容')
    tags = models.ManyToManyField(Tag,verbose_name=u'文章标签')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name=u'文章'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.title
