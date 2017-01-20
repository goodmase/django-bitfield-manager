# -*- coding: utf-8
from django.apps import AppConfig


class BitfieldManagerConfig(AppConfig):
    name = 'bitfield_manager'

    def ready(self):
        import bitfield_manager.signals # noqa
