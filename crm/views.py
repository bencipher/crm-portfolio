from gateway.auth import Authentication
from .serializers import AgentSerializer, LeadSerializer
from .models import Lead, Agent
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class AgentViewset(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()


class LeadViewset(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    queryset = Lead.objects.all()
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        data = request.data
        if data.get('assignee'):
            assignee = Agent.objects.get(id=data.pop('assignee'))
            data['assignee'] = assignee
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
def convert_lead_to_customer(requests, *args, **kwargs):
    id = requests.data.get("lead")
    if not id:
        return Response({"status": 400, "message": "lead is required required"})

    lead = Lead.objects.filter(id=id).first()
    if not lead:
        return Response({"status": 400, "message": "Invalid lead id"})

    try:
        lead.is_customer = True
    except Exception as e:
        return Response({"status": 400, "message": str(e)})
    return Response({"status": 200, "message": lead})
