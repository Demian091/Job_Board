from rest_framework import generics, permissions, filters
from django.urls import path, include
from apps.companies.models import Company
from apps.api.serializers.companies import (
    CompanyListSerializer, CompanyDetailSerializer, CompanyCreateSerializer
)
from apps.api.permissions import IsEmployer

class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.filter(is_verified=True)
    serializer_class = CompanyListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'industry', 'location']

class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'slug'

class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanyCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CompanyUpdateView(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)

class MyCompanyView(generics.RetrieveAPIView):
    serializer_class = CompanyDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    
    def get_object(self):
        return self.request.user.company

urlpatterns = [
    path('', CompanyListView.as_view(), name='api_company_list'),
    path('my-company/', MyCompanyView.as_view(), name='api_my_company'),
    path('create/', CompanyCreateView.as_view(), name='api_company_create'),
    path('<slug:slug>/', CompanyDetailView.as_view(), name='api_company_detail'),
    path('<slug:slug>/update/', CompanyUpdateView.as_view(), name='api_company_update'),
]
