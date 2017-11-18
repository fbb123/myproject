# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'apps.user_operation'

    def ready(self):
        import user_operation.signals

