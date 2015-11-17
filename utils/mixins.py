from django.db.models.fields import AutoField, related

from utils.functions import underscore_dict, get_val_or_none

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

class CreateableFromAttrsMixin(object):
    """
    Mixin for model manager classes.
    """
    def init_dict(self, kwargs):
        """
        Accepts kwargs in snakeCase (as presented by Riot's API) and returns an
        initialization dict that contains just the fields and values that are relevant
        to this model.
        """
        model_fields = [f for f in self.model.data_fields()]
        underscore_kwargs = underscore_dict(kwargs)
        dct = {}

        for field in model_fields:
            dct[field] = underscore_kwargs[field]

        return dct

class ParticipantFromAttrsMixin(object):
    """
    A mixin for the Participant model manager to handle the merging of
    Riot's ParticipantStats DTO's fields into Participant.
    """
    def init_dict(self, attrs):
        """
        Return an initialization dict that contains just the key-value
        pairs that are relevant to the Participant model.
        """
        # The fields that Riot sends as part of the Participant DTO,
        # as opposed to the ParticipantStats DTO.
        native_field_names = ['champion_id',
                              'highest_achieved_season_tier',
                              'participant_id',
                              'spell1_id',
                              'spell2_id',
                              'team_id']

        # We construct sets of field names to determine which fields come from
        # which DTO via set differences (there are a lot of fields in
        # ParticipantStats and it can easily change).
        native_fields_set = set(native_field_names)

        model_fields = [f for f in self.model.data_fields()]
        all_fields_set = set(model_fields)

        # ParticipantStats will always contain whatever isn't in Participant.
        stats_fields = all_fields_set - native_fields_set

        underscore_attrs = underscore_dict(attrs)

        # We will be populating `dct` with the total fields required to
        # init the Participant instance.
        dct = {}

        # First, set the fields that come from the Participant DTO.
        for k in native_field_names:
            dct[k] = underscore_attrs[k]

        # Participant also contains fields from Riot's ParticipantStats DTO
        # (we store both DTOs' fields in a single model - Participant),
        # so here we get the ParticipantStats fields and insert them into
        # the top level of the returned dict.
        valid_stats_dct = {}
        stats_attrs = underscore_dict(attrs['stats'])

        # We can't just use the underscore converted attrs['stats'] b/c Riot
        # omits fields that would be empty/0/null, so we replace empty fields
        # with None.
        for k in stats_fields:
            valid_stats_dct[k] = get_val_or_none(stats_attrs, k)

        dct.update(valid_stats_dct)

        return dct