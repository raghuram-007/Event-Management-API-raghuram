from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RSVPViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'rsvps', RSVPViewSet,basename='rsvp')
router.register(r'reviews', ReviewViewSet,basename='review')

urlpatterns = [
    
    path('events/<int:event_id>/rsvp/', RSVPViewSet.as_view({'post': 'create'})),
    path('events/<int:event_id>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('events/<int:event_id>/rsvp/<int:pk>/', RSVPViewSet.as_view({'patch': 'partial_update'})),

    path('', include(router.urls)),
]
