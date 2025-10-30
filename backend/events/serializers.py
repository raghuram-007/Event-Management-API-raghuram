from rest_framework import serializers
from .models import Event, RSVP, Review, UserProfile
from django.contrib.auth.models import User


# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class UserProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'full_name', 'bio', 'location', 'profile_picture']


# --- Event Serializer ---
class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


# --- RSVP Serializer ---
class RSVPSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RSVP
        fields =['id', 'event', 'user', 'status', 'created_at']


# --- Review Serializer ---
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'event', 'user', 'rating', 'comment', 'created_at']
