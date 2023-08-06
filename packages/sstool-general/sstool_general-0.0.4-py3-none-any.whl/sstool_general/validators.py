def min_str_len(instance, attribute, value):
    min_length = attribute.metadata.get('min_length', None)
    if len(value) <= min_length:
        raise ValueError(
            '{0} must have a minimum length of {1} chars'.format(
                attribute.name, min_length
            )
        )


def max_str_len(instance, attribute, value):
    max_length = attribute.metadata.get('max_length', None)
    if len(value) > max_length:
        raise ValueError(
            '{0} must have a maximum length of {1} chars'.format(
                attribute.name, max_length
            )
        )


def min_max_str_len(instance, attribute, value):
    min_str_len(instance, attribute, value)
    max_str_len(instance, attribute, value)


def min_number(instance, attribute, value):
    minimum = attribute.metadata.get('minimum', None)
    if value <= minimum:
        raise ValueError(
            '{0} must be more than {1}'.format(
                attribute.name, minimum
            )
        )


def max_number(instance, attribute, value):
    maximum = attribute.metadata.get('maximum', None)
    if value > maximum:
        raise ValueError(
            '{0} must be less than {1}'.format(
                attribute.name, maximum
            )
        )


def min_max_number(instance, attribute, value):
    min_number(instance, attribute, value)
    max_number(instance, attribute, value)
