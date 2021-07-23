from django.contrib import admin
from .models import RatedAudio,Rating
# Register your models here.
admin.site.register(RatedAudio)
admin.site.register(Rating)