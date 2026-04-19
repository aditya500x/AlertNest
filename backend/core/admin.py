from django.contrib import admin
from .models import Incident, ChatMessage

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('type', 'severity', 'location', 'status', 'created_at')
    list_filter = ('type', 'severity', 'status')
    search_fields = ('text', 'location')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'incident', 'timestamp')
    search_fields = ('sender', 'message')
