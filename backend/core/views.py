from django.shortcuts import render
import datetime
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import viewsets
from .serializers import RatingSerializer,RatedAudioSerializer,RatedAudioDataSerializer
from .models import RatedAudio,Rating
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.parsers import MultiPartParser


from rest_framework_bulk import (
    BulkModelViewSet,
    BulkCreateModelMixin
)

    
class RatedAudioViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = RatedAudio.objects.filter(Q(status=1))
    serializer_class = RatedAudioSerializer

    @action(
        detail=True,
        methods=['PUT'],
        serializer_class=RatedAudioDataSerializer,
        parser_classes=[MultiPartParser],
    )

    def audio(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                                 status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = RatedAudio.objects.filter(Q(status=1) & ~Q(audio_ratings__rater=request.user))
        ratings=Rating.objects.filter(rater=request.user).values_list('audio')
        print(ratings)
        l=len(queryset)
        queryset=queryset[:min(l,10)] #handle if length of queryset is less than 10
        print(queryset)
        serializer=RatedAudioSerializer(queryset,context={'request':request},many=True)
        data=serializer.data
        return Response(data)

class RatingViewSet(BulkModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Rating.objects.filter()
    serializer_class = RatingSerializer

    
    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.data, list)

        if not bulk: #for single
            request.data['rater']=request.user.id
            update_avg_rating_cnt(request.data)
            return super(BulkCreateModelMixin, self).create(request, *args, **kwargs)

        else: # For list or bulk
            print(request.data)
            for d in request.data:
                d['rater']=request.user.id
            print(request.data)
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)
            update_avg_rating_cnt(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

def update_avg_rating_cnt(instances):
    if isinstance(instances, list): #For list of instances
        for instance in instances:
            audio_id = instance["audio"]
            obj=RatedAudio.objects.get(pk=audio_id)
            rating_cnt=obj.rating_cnt
            prev_avg=obj.avg_rating
            print(float(instance["value"]))
            avg=((rating_cnt*prev_avg)+float(instance["value"]))/(rating_cnt+1)
            obj.avg_rating = avg
            obj.rating_cnt+=1
            obj.save()
    else:#for single instance
        instance=instances
        audio_id = instance["audio"]
        obj=RatedAudio.objects.get(pk=audio_id)
        rating_cnt=obj.rating_cnt
        prev_avg=obj.avg_rating
        print(float(instance["value"]))
        avg=((rating_cnt*prev_avg)+float(instance["value"]))/(rating_cnt+1)
        obj.avg_rating = avg
        obj.rating_cnt+=1
        obj.save()

