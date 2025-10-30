from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Event, RSVP, Review


class EventAPITests(APITestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='raghu', password='testpass')
        self.other_user = User.objects.create_user(username='guest', password='guestpass')
        self.invited_user = User.objects.create_user(username='invited', password='invitedpass')

        # Authenticate user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a public event
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event.",
            organizer=self.user,
            location="Chennai",
            start_time="2025-10-30T10:00:00Z",
            end_time="2025-10-30T12:00:00Z",
            is_public=True
        )

        # Create a private event with an invited user
        self.private_event = Event.objects.create(
            title="Private Event",
            description="Invite-only event.",
            organizer=self.user,
            location="Mumbai",
            start_time="2025-11-01T15:00:00Z",
            end_time="2025-11-01T17:00:00Z",
            is_public=False
        )
        self.private_event.invited_users.add(self.invited_user)

    def test_list_events(self):
        """✅ Test fetching public events"""
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_create_event(self):
        """✅ Test creating a new event"""
        url = reverse('event-list')
        data = {
            "title": "New Event",
            "description": "Created via test case",
            "location": "Bangalore",
            "start_time": "2025-10-31T08:00:00Z",
            "end_time": "2025-10-31T10:00:00Z",
            "is_public": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 3)

    def test_update_event_by_non_organizer(self):
        """❌ Test that other users cannot update someone else's event"""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('event-detail', args=[self.event.id])
        response = self.client.put(url, {"title": "Hack Attempt"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_by_organizer(self):
        """✅ Organizer should be able to delete their event"""
        url = reverse('event-detail', args=[self.event.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_rsvp_to_event(self):
        """✅ Test user can RSVP to an event"""
        url = f"/api/events/{self.event.id}/rsvp/"
        data = {"status": "Going"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RSVP.objects.count(), 1)

    def test_add_review_to_event(self):
        """✅ Test user can add a review for an event"""
        url = f"/api/events/{self.event.id}/reviews/"
        data = {"rating": 5, "comment": "Awesome event!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_private_event_visibility(self):
        """🟡 Bonus Test — Ensure private events are visible only to organizer or invited users"""
        # Organizer can see
        self.client.force_authenticate(user=self.user)
        url = reverse('event-list')
        response = self.client.get(url)
        event_titles = [e['title'] for e in response.data['results']]
        self.assertIn("Private Event", event_titles)

        # Invited user can see
        self.client.force_authenticate(user=self.invited_user)
        response = self.client.get(url)
        event_titles = [e['title'] for e in response.data['results']]
        self.assertIn("Private Event", event_titles)

        # Other user cannot see
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(url)
        event_titles = [e['title'] for e in response.data['results']]
        self.assertNotIn("Private Event", event_titles)
