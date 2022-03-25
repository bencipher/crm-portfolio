from django.urls import path, include, re_path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'agents', AgentViewset, basename='agents')
router.register(r'leads', LeadViewset, basename='leads')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('', convert_lead_to_customer, name='convert-lead'),
]
