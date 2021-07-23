from django.db import models
from datetime import datetime,timedelta    
from django.utils import timezone
from django.contrib.auth.models import User

class RatedAudio(models.Model):
    audio=models.FileField(upload_to="rated_sounds", blank=True, null=True)
    rating_precision=models.FloatField(default=1)
    lower_limit=models.IntegerField(default=1)
    upper_limit=models.IntegerField(default=5)
    label=models.CharField(max_length=200,null=True,blank=True)
    avg_rating=models.FloatField(default=0.0,null=True,blank=True)
    status=models.IntegerField(default=1,null=True,blank=True)
    rating_cnt=models.IntegerField(default=0,null=True,blank=True)

class Rating(models.Model):
    value=models.CharField(max_length=3,blank=True, null=True)
    remarks=models.CharField(max_length=500,null=True,blank=True)
    suggested_label=models.CharField(max_length=100,null=True,blank=True)
    rater=models.ForeignKey(User, related_name='rater_ratings',on_delete=models.SET_NULL,null=True,blank=True)
    audio=models.ForeignKey(RatedAudio,related_name='audio_ratings',on_delete=models.CASCADE)

    


