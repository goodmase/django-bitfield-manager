# AND
def is_flag_set_for_status(status, flag):
    return (status & flag) == flag


def is_flag_field_set_for_status(status, flag_field):
    return is_flag_set_for_status(status, (1 << flag_field))


def unset_flag_field_for_status(status, flag_field):
    return unset_flag_for_status(status, (1 << flag_field))


def unset_flag_for_status(status, flag):
    return status & ~flag


# OR
def set_flag_for_status(status, flag):
    return status | flag


def set_flag_field_for_status(status, flag_field):
    return set_flag_for_status(status, (1 << flag_field))


def get_all_related_bitfield_models(model):
    return [
        f.related_model for f in model._meta.get_fields()
        if
        not (not (f.one_to_many or f.one_to_one) or not f.auto_created) and not f.concrete and hasattr(f.related_model,
                                                                                                       'BitfieldMeta')
        ]
