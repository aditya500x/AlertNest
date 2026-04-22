from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os


from .models import Incident, ChatMessage
from .serializers import IncidentSerializer, ChatMessageSerializer
from .utils import classify_incident, extract_location

class IncidentListView(APIView):
    def get(self, request):
        incidents = list(Incident.objects.filter(status='ACTIVE'))
        
        if not incidents:
            return Response([])
            
        # 1. Prepare data for the EPE
        from .epe import EmergencyPriorityEngine
        engine = EmergencyPriorityEngine()
        
        epe_payload = []
        for inc in incidents:
            time_diff = (timezone.now() - inc.created_at).total_seconds() / 60.0
            epe_payload.append({
                "id": inc.id,
                "text": inc.text,
                "people_affected": 0, # Could be extracted from text later
                "people_at_risk": 0,
                "time_reported_mins": max(0, time_diff)
            })
            
        # 2. Run EPE Inference
        ranked_output = engine.rank_emergencies(epe_payload)
        ranked_items = ranked_output.get("prioritized_emergencies", [])
        ranked_ids = [item["id"] for item in ranked_items]
        
        # 3. Sort backend models matching EPE rank
        incident_map = {inc.id: inc for inc in incidents}
        sorted_incidents = []
        for r_id in ranked_ids:
            if r_id in incident_map:
                sorted_incidents.append(incident_map[r_id])
                
        # 4. Fallback for any unranked items
        for inc in incidents:
            if inc.id not in ranked_ids:
                sorted_incidents.append(inc)

        # 5. Serialize and inject EPE data
        serializer = IncidentSerializer(sorted_incidents, many=True)
        response_data = serializer.data
        
        for item in response_data:
            for r_item in ranked_items:
                if r_item["id"] == item["id"]:
                    item["epe_score"] = r_item["priority_score"]
                    item["epe_reason"] = r_item["reason"]
                    break
                    
        return Response(response_data)

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
