from gateway.auth import Authentication
from users.models import CustomUser
from .serializers import AgentSerializer, LeadSerializer
from .models import Lead, Agent
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class AgentViewset(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AgentSerializer
    queryset = Agent.objects.select_related('user')

    def destroy(self, request, *args, **kwargs):
        try:
            CustomUser.objects.filter(email=request.data.get('email')).delete()
        except Exception:
            raise Exception('cannot delete user')
        return super(AgentViewset, self).destroy(request, *args, **kwargs)


class LeadViewset(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    queryset = Lead.objects.select_related('assignee')
    authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
