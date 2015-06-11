from django.db.models.fields import AutoField

class IterableNonAutoFieldsMixin(object):
    """
    Mixin for model classes.
    """
    @classmethod
    def non_autofields(cls):
        """
        Generator that yields all fields of cls, except AutoFields.
        """
        for field in cls._meta.fields:
            if type(field) is not AutoField:
                yield field.name