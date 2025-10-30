from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer



## --- Event ViewSet ---
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'organizer__username']  # ✅ Filtering
    search_fields = ['title', 'location', 'organizer__username']  # ✅ Searching
    ordering_fields = ['created_at', 'start_time', 'end_time']  # ✅ Ordering fields
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        """✅ Restrict private events to organizer only"""
        user = self.request.user

        queryset = Event.objects.filter(is_public=True)
        if user.is_authenticated:
            own_events = Event.objects.filter(organizer=user)
            invited_events = Event.objects.filter(invited_users=user)
            queryset = queryset | own_events | invited_events
        return queryset.distinct()

    # ✅ Fix: move permission check before serializer validation
    def update(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user:
            raise PermissionDenied('You can only edit your own events.')
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance.organizer != self.request.user:
            raise PermissionDenied('You can only delete your own events.')
        instance.delete()


# --- RSVP ViewSet ---
class RSVPViewSet(viewsets.ModelViewSet):
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if event_id:
            return RSVP.objects.filter(event_id=event_id)
        return RSVP.objects.all()

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        if event_id:
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                raise PermissionDenied('Event not found.')
            # ✅ Save with actual event object
            serializer.save(user=self.request.user, event=event)
        else:
            serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        """PATCH /events/{event_id}/rsvp/{user_id}/ — Update RSVP status"""
        event_id = self.kwargs.get('event_id')
        user_id = self.kwargs.get('pk')  # 'pk' = RSVP record ID

        rsvp = get_object_or_404(RSVP, id=user_id, event_id=event_id)

        # ✅ Only the RSVP owner can update
        if rsvp.user != request.user:
            raise PermissionDenied("You can only update your own RSVP.")

        serializer = self.get_serializer(rsvp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# --- Review ViewSet ---
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if event_id:
            return Review.objects.filter(event_id=event_id).order_by('-created_at')
        return Review.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        if event_id:
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                raise PermissionDenied('Event not found.')
            # ✅ Save review linked to event
            serializer.save(user=self.request.user, event=event)
        else:
            serializer.save(user=self.request.user)
