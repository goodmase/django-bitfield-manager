# -*- coding: utf-8 -*-

from django.db import models

from bitfield_manager import utils


class ParentBitfieldModelMixin(object):
    def set_flag(self, status_field, flag, save=False):
        status_value = getattr(self, status_field)
        status_value = utils.set_flag_field_for_status(status_value, flag)
        setattr(self, status_field, status_value)
        if save:
            self.save()
        return self

    def unset_flag(self, status_field, flag, save=False):
        status_value = getattr(self, status_field)
        status_value = utils.unset_flag_field_for_status(status_value, flag)
        setattr(self, status_field, status_value)
        if save:
            self.save()
        return self

    def force_status_refresh(self, related_models=None, search_depth=1):
        if not related_models:
            related_models = utils.get_all_related_bitfield_models(self.__class__, search_depth=search_depth)
        for i in related_models:
            parent_models = i.BitfieldMeta.parent_models
            for parent, field, flag in parent_models:
                parent = parent.replace(".", "__")
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


class ChildBitfieldModelMixin(object):
    def save(self, *args, **kwargs):
        if not hasattr(self, 'BitfieldMeta'):
            super(ChildBitfieldModelMixin, self).save(*args, **kwargs)
            return
        parent_models = self.BitfieldMeta.parent_models

        for parent, field, flag in parent_models:
            parent_model = utils.get_parent_model(self, parent)

            if not parent_model or parent_model.__class__.__name__ == 'ManyRelatedManager':
                # don't bother with m2m on save.
                continue
            else:
                utils.check_and_set_flag(parent_model, field, flag)
        super(ChildBitfieldModelMixin, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not hasattr(self, 'BitfieldMeta'):
            return super(ChildBitfieldModelMixin, self).delete(*args, **kwargs)

        parent_models = self.BitfieldMeta.parent_models
        for parent, field, flag in parent_models:
            parent_model = utils.get_parent_model(self, parent)
            if not parent_model or parent_model.__class__.__name__ == 'ManyRelatedManager':
                # don't bother with m2m on delete
                continue
            # replace the dot syntac with underscore for getting child count
            parent = parent.replace('.', '__')
            status_value = getattr(parent_model, field)
            if utils.is_flag_field_set_for_status(status_value, flag):
                # if it is set then check the count of the child model
                # if only 1 or less left unset the flag
                child_count = self.__class__.objects.filter(**{parent: parent_model.id}).count()
                if child_count <= 1:
                    status_value = utils.unset_flag_field_for_status(status_value, flag)
                    setattr(parent_model, field, status_value)
                    parent_model.save(update_fields=[field])
        return super(ChildBitfieldModelMixin, self).delete(*args, **kwargs)


class ParentBitfieldModel(ParentBitfieldModelMixin, models.Model):
    pass
