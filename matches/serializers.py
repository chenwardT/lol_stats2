import logging

from rest_framework import serializers

from summoners.models import Summoner
from .models import (MatchDetail,
                     Participant,
                     ParticipantIdentity,
                     Team,
                     Mastery,
                     ParticipantTimeline,
                     Rune,
                     BannedChampion)

logger = logging.getLogger(__name__)


class SimplifiedSummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        fields = ('name',)


class MasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mastery
        fields = [f for f in Mastery.data_fields()]


class RuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rune
        fields = [f for f in Rune.data_fields()]


class BannedChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedChampion
        fields = [f for f in BannedChampion.data_fields()]


class TeamSerializer(serializers.ModelSerializer):
    bannedchampion_set = BannedChampionSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [f for f in Team.data_fields()] + ['bannedchampion_set']


class ParticipantTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantTimeline
        fields = [f for f in ParticipantTimeline.data_fields()]


class ParticipantSerializer(serializers.ModelSerializer):
    # rune_set = RuneSerializer(many=True, read_only=True)
    # mastery_set = MasterySerializer(many=True, read_only=True)
    participanttimeline_set = ParticipantTimelineSerializer(many=True, read_only=True)

    class Meta:
        model = Participant
        fields = [f for f in Participant.data_fields()] + [#'rune_set',
                                                           #'mastery_set',
                                                           'participanttimeline_set']


class ParticipantIdentitySerializer(serializers.ModelSerializer):
    summoner = SimplifiedSummonerSerializer(read_only=True)

    class Meta:
        model = ParticipantIdentity
        fields = ('participant_id', 'summoner')


class MatchDetailSerializer(serializers.ModelSerializer):
    participantidentity_set = ParticipantIdentitySerializer(many=True, read_only=True)
    participant_set = ParticipantSerializer(many=True, read_only=True)
    team_set = TeamSerializer(many=True, read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        """
        Perform necessary eager loading of data.
        """
        queryset = queryset.prefetch_related('participantidentity_set',
                                             'participantidentity_set__summoner',
                                             'participant_set',
                                             'participant_set__participanttimeline_set',
                                             'team_set',
                                             'team_set__bannedchampion_set')

        return queryset

    class Meta:
        model = MatchDetail
        fields = [f for f in MatchDetail.data_fields()] + ['participantidentity_set',
                                                           'participant_set',
                                                           'team_set']
