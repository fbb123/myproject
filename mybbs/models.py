# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    user = models.ForeignKey()
