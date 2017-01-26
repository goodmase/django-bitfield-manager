try:
    from bitfield.types import Bit, BitHandler
except:
    Bit = None
    BitHandler = None


# AND
def is_flag_set_for_status(status, flag):
    # this is because checking for equality on bithandlers will return false
    # when compared to an int of the same value
    if BitHandler and type(status) == BitHandler:
        status = int(status)
    return (status & flag) == flag


def is_flag_field_set_for_status(status, flag_field):
    if Bit and type(flag_field) == Bit:
        return is_flag_set_for_status(status, flag_field.mask)
    return is_flag_set_for_status(status, (1 << flag_field))


def unset_flag_field_for_status(status, flag_field):
    if Bit and type(flag_field) == Bit:
        return unset_flag_for_status(status, flag_field.mask)
    return unset_flag_for_status(status, (1 << flag_field))


def unset_flag_for_status(status, flag):
    return status & ~flag


# OR
def set_flag_for_status(status, flag):
    return status | flag


def set_flag_field_for_status(status, flag_field):
    if Bit and type(flag_field) == Bit:
        # django-bitfield has the field already shifted
        return set_flag_for_status(status, flag_field.mask)
    return set_flag_for_status(status, (1 << flag_field))


def get_all_related_bitfield_models(model, all_models=[], search_depth=1, current_level=0):
    # recursive function to get models multiple levels deep
    new_models = [f.related_model for f in model._meta.get_fields() if
                  f.auto_created and not f.concrete and hasattr(f.related_model, 'BitfieldMeta')]
    if search_depth == 1:
        return new_models

    for m in new_models:
        all_models.append(m)
        if current_level <= search_depth:
            current_level += 1
            get_all_related_bitfield_models(m, all_models, search_depth=search_depth, current_level=current_level)
    return all_models


def get_parent_model(instance, key_string):
    keys = key_string.split('.')
    for key in keys:
        instance = getattr(instance, key)
    return instance


def check_and_set_flag(parent_model, field, flag):
    status_value = getattr(parent_model, field)
    if not is_flag_field_set_for_status(status_value, flag):
        status_value = set_flag_field_for_status(status_value, flag)
        setattr(parent_model, field, status_value)
        parent_model.save(update_fields=[field])
