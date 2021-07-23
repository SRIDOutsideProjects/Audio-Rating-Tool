from django.urls import include, path
from rest_framework import routers
from . import views
router = routers.SimpleRouter()
router.register(r'ratedaudios', views.RatedAudioViewSet)
router.register(r'rating', views.RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
