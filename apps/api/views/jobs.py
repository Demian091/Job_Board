from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.urls import path, include
from django.db.models import Q
from apps.jobs.models import Job
from apps.api.serializers.jobs import (
    JobListSerializer, JobDetailSerializer, JobCreateSerializer
)
from apps.api.permissions import IsEmployer

class JobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'company__name']
    ordering_fields = ['created_at', 'salary_min', 'views_count']
    
    def get_queryset(self):
        queryset = Job.objects.filter(
            status='active',
            expires_at__gt=timezone.now()
        ).select_related('company')
        
        # Filters
        job_type = self.request.query_params.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        experience = self.request.query_params.get('experience')
        if experience:
            queryset = queryset.filter(experience_level=experience)
        
        remote = self.request.query_params.get('remote')
        if remote:
            queryset = queryset.filter(is_remote=True)
        
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__slug=company)
        
        return queryset

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobDetailSerializer
    lookup_field = 'slug'
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        Job.objects.filter(pk=obj.pk).update(views_count=models.F('views_count') + 1)
        return obj

class JobCreateView(generics.CreateAPIView):
    serializer_class = JobCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    
    def perform_create(self, serializer):
        serializer.save(
            posted_by=self.request.user,
            company=self.request.user.company
        )

class JobUpdateView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

class JobDeleteView(generics.DestroyAPIView):
    queryset = Job.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

class MyJobsView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

@api_view(['GET'])
def job_types(request):
    return Response(dict(Job.JOB_TYPES))

@api_view(['GET'])
def experience_levels(request):
    return Response(dict(Job.EXPERIENCE_LEVELS))

urlpatterns = [
    path('', JobListView.as_view(), name='api_job_list'),
    path('types/', job_types, name='api_job_types'),
    path('experience-levels/', experience_levels, name='api_experience_levels'),
    path('my-jobs/', MyJobsView.as_view(), name='api_my_jobs'),
    path('create/', JobCreateView.as_view(), name='api_job_create'),
    path('<slug:slug>/', JobDetailView.as_view(), name='api_job_detail'),
    path('<slug:slug>/update/', JobUpdateView.as_view(), name='api_job_update'),
    path('<slug:slug>/delete/', JobDeleteView.as_view(), name='api_job_delete'),
]
