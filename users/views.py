from .serializers import CustomUserSerializer
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets


class CustomUserViewset(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'id'




# class RegisterView(APIView):
#     """Register Endpoint"""
#     custom_user_model = get_user_model()
#     serializer_class = CustomUserSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.custom_user_model.objects.create_user(**serializer.validated_data)
#
#         return Response({
#             "Success": f"User {serializer.validated_data['name']} created successfully"
#         },
#             status=status.HTTP_201_CREATED)
