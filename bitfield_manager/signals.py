from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from bitfield_manager import utils


@receiver(post_save)
def bitfield_post_save(sender, instance, **kwargs):
    if not hasattr(sender, 'BitfieldMeta'):
        return
    parent_models = instance.BitfieldMeta.parent_models

    for parent, field, flag in parent_models:
        parent_model = utils.get_parent_model(instance, parent)
        if parent_model.__class__.__name__ == 'ManyRelatedManager':
            # don't bother with m2m on save.
            continue
        else:
            utils.check_and_set_flag(parent_model, field, flag)


@receiver(post_delete)
def bitfield_post_delete(sender, instance, **kwargs):
    if not hasattr(sender, 'BitfieldMeta'):
        return

    parent_models = instance.BitfieldMeta.parent_models
    for parent, field, flag in parent_models:
        parent_model = utils.get_parent_model(instance, parent)
        # replace the dot syntac with underscore for getting child count
        parent = parent.replace('.', '__')
        if parent_model.__class__.__name__ == 'ManyRelatedManager':
            # don't both with m2m on delete
            continue
        status_value = getattr(parent_model, field)
        if utils.is_flag_field_set_for_status(status_value, flag):
            # if it is set then check the count of the child model
            child_count = sender.objects.filter(**{parent: parent_model.id}).count()
            if child_count == 0:
                status_value = utils.unset_flag_field_for_status(status_value, flag)
                setattr(parent_model, field, status_value)
                parent_model.save(update_fields=[field])
