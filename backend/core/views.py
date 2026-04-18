from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os
from groq import Groq

from .models import Incident, ChatMessage
from .serializers import IncidentSerializer, ChatMessageSerializer
from .utils import classify_incident, extract_location

class IncidentListView(APIView):
    def get(self, request):
        incidents = Incident.objects.filter(status='ACTIVE')
        # Sort HIGH > MEDIUM > LOW
        sev_map = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        sorted_incidents = sorted(incidents, key=lambda x: sev_map.get(x.severity, 0), reverse=True)
        serializer = IncidentSerializer(sorted_incidents, many=True)
        return Response(serializer.data)

class IncidentCreateView(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        if not text:
            return Response({"detail": "Missing text"}, status=status.HTTP_400_BAD_REQUEST)
            
        inc_type, inc_severity = classify_incident(text)
        location = extract_location(text)
        
        incident = Incident.objects.create(
            text=text,
            type=inc_type,
            severity=inc_severity,
            location=location,
            status="ACTIVE"
        )
        
        # Broadcast
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "alerts",
            {
                "type": "broadcast_event",
                "payload": {
                    "event": "new_incident",
                    "data": {
                        "id": incident.id,
                        "type": incident.type,
                        "severity": incident.severity,
                        "location": incident.location,
                        "status": incident.status
                    }
                }
            }
        )
        
        serializer = IncidentSerializer(incident)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class IncidentAudioCreateView(APIView):
    def post(self, request):
        if 'audio' not in request.FILES:
            return Response({"detail": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_file = request.FILES['audio']
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return Response({"detail": "GROQ_API_KEY not configured in backend"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        client = Groq(api_key=api_key)
        
        try:
            translation = client.audio.translations.create(
                file=(audio_file.name, audio_file.read()),
                model="whisper-large-v3",
            )
            text = translation.text
        except Exception as e:
            return Response({"detail": f"Translation failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if not text:
            return Response({"detail": "No speech detected"}, status=status.HTTP_400_BAD_REQUEST)
            
        print(f"Whisper Translated Text: {text}")
            
        inc_type, inc_severity = classify_incident(text)
        location = extract_location(text)
        
        incident = Incident.objects.create(
            text=text,
            type=inc_type,
            severity=inc_severity,
            location=location,
            status="ACTIVE"
        )
        
        # Broadcast
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "alerts",
            {
                "type": "broadcast_event",
                "payload": {
                    "event": "new_incident",
                    "data": {
                        "id": incident.id,
                        "type": incident.type,
                        "severity": incident.severity,
                        "location": incident.location,
                        "status": incident.status
                    }
                }
            }
        )
        
        serializer = IncidentSerializer(incident)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class IncidentResolveView(APIView):
    def post(self, request, pk):
        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
            
        incident.status = "RESOLVED"
        incident.resolved_at = timezone.now()
        incident.save()
        
        # Broadcast
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "alerts",
            {
                "type": "broadcast_event",
                "payload": {
                    "event": "incident_resolved",
                    "data": {"id": pk}
                }
            }
        )
        return Response({"success": True})

class ChatView(APIView):
    def get(self, request, incident_id):
        messages = ChatMessage.objects.filter(incident_id=incident_id).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
        
    def post(self, request, incident_id):
        try:
            incident = Incident.objects.get(pk=incident_id)
        except Incident.DoesNotExist:
            return Response({"detail": "Incident Not Found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            msg = serializer.save(incident=incident)
            
            # Broadcast
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "alerts",
                {
                    "type": "broadcast_event",
                    "payload": {
                        "event": "chat_message",
                        "data": {
                            "incident_id": incident_id,
                            "sender": msg.sender,
                            "message": msg.message
                        }
                    }
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
