from gateway.auth import Authentication
from .serializers import AgentSerializer, LeadSerializer
from .models import Lead, Agent
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class AgentViewset(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AgentSerializer
    queryset = Agent.objects.select_related('user')


class LeadViewset(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    queryset = Lead.objects.select_related('assignee')
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
