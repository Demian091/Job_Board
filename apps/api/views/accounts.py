from django.urls import path
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.accounts.models import User
from apps.api.serializers.accounts import (
    UserSerializer, UserCreateSerializer, ProfileUpdateSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_type_check(request):
    return Response({
        'user_type': request.user.user_type,
        'is_employer': request.user.user_type == 'employer',
        'is_jobseeker': request.user.user_type == 'jobseeker',
    })

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='api_profile_update'),
    path('type/', user_type_check, name='api_user_type'),
]
