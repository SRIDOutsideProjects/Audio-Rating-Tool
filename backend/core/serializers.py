# serializers.py
from rest_framework import serializers

from .models import RatedAudio,Rating

from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin
)

class RatedAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatedAudio
        fields = '__all__'

class RatingSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model = Rating
        list_serializer_class = BulkListSerializer
        fields = ('value','remarks','audio','rater')


class RatedAudioDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=RatedAudio
        fields=('audio',)