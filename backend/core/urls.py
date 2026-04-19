from django.urls import path
from .views import IncidentListView, IncidentCreateView, IncidentResolveView, ChatView, IncidentAudioCreateView

urlpatterns = [
    path('incidents/', IncidentListView.as_view(), name='incident-list'),
    path('incident/', IncidentCreateView.as_view(), name='incident-create'),
    path('incident/audio/', IncidentAudioCreateView.as_view(), name='incident-audio-create'),
    path('incident/<int:pk>/resolve/', IncidentResolveView.as_view(), name='incident-resolve'),
    path('incident/<int:incident_id>/chat/', ChatView.as_view(), name='chat'),
]
