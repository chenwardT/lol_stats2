from django.db.models.fields import AutoField, related

from utils.functions import underscore_dict

class IterableDataFieldsMixin(object):
    """
    Mixin for model classes.
    """
    @classmethod
    def data_fields(cls):
        """
        Generator that yields all fields of instances of type cls that should
        be filled in with data from attrs, i.e. fields of type other than AutoField,
        ForeignKey (FKs would point to data that goes in a different model).

        See matches.models manager classes' `create_` methods.
        """
        for field in cls._meta.fields:
            if type(field) is not AutoField and type(field) is not related.ForeignKey:
                yield field.name

class CreatebleFromAttrsMixin(object):
    """
    Mixin for model manager classes.
    """
    def init_dict(self, attrs):
        """
        Return an initialization dict that contains just the key-value
        pairs that are relevant to this model.
        """
        model_fields = [f for f in self.model.data_fields()]
        underscore_attrs = underscore_dict(attrs)
        dct = {}

        for k in model_fields:
            dct[k] = underscore_attrs[k]

        return dct
