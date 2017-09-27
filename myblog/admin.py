# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category,Tag,Post
# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)