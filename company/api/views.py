from rest_framework import generics
from .serializers import RegisterSerializer
from company.models import User

class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
