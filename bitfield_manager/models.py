# -*- coding: utf-8 -*-

from django.db import models
from bitfield_manager import utils


class ParentBitfieldModelMixin(object):
    def force_status_refresh(self, related_models=None):
        if not related_models:
            related_models = utils.get_all_related_bitfield_models(self.__class__)
        for i in related_models:
            parent_models = i.BitfieldMeta.parent_models
            for parent, field, flag in parent_models:
                related_count = i.objects.filter(**{parent: self.id}).count()
                status_value = getattr(self, field)
                if related_count == 0 and utils.is_flag_field_set_for_status(status_value, flag):
                    status_value = utils.unset_flag_field_for_status(status_value, flag)
                    setattr(self, field, status_value)
                    self.save(update_fields=[field])
                elif related_count > 0 and not utils.is_flag_field_set_for_status(status_value, flag):
                    status_value = utils.set_flag_field_for_status(status_value, flag)
                    setattr(self, field, status_value)
                    self.save(update_fields=[field])
        return self


class ParentBitfieldModel(ParentBitfieldModelMixin, models.Model):
    pass
