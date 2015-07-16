from google.protobuf import internal


def protobuf_to_dict(pb_value):
    result = {}
    for name in pb_value.DESCRIPTOR.fields_by_name.keys():
        value = getattr(pb_value, name)
        if isinstance(
                value,
                internal.containers.RepeatedCompositeFieldContainer):
            value = list(value)
        result[name] = value
    return result
