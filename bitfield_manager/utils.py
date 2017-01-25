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


def get_all_related_bitfield_models(model):
    return [
        f.related_model for f in model._meta.get_fields()
        if
        not (not (f.one_to_many or f.one_to_one) or not f.auto_created) and not f.concrete and hasattr(f.related_model,
                                                                                                       'BitfieldMeta')
        ]


def get_parent_model(instance, key_string):
    keys = key_string.split('.')
    for key in keys:
        instance = getattr(instance, key)
    return instance
