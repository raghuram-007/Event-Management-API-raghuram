from django.contrib import admin
from .models import*

# Register your models here.
@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display=('user', 'full_name', 'location')
    list_filter=('location',)
    
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=('title', 'organizer', 'location', 'start_time', 'end_time', 'is_public')
    search_fields = ('title', 'location', 'organizer__username')
    list_filter = ('is_public', 'start_time')
    
    


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'rating', 'created_at')
    search_fields = ('event__title', 'user__username')


