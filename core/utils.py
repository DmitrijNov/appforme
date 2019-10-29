from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return None
