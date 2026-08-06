from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.urls import path, include
from django.db.models import Q, F
from apps.applications.models import Application
from apps.jobs.models import Job
from apps.api.serializers.applications import (
    ApplicationListSerializer, ApplicationDetailSerializer,
    ApplicationCreateSerializer, ApplicationStatusSerializer
)

class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'jobseeker':
            return Application.objects.filter(applicant=self.request.user)
        else:
            return Application.objects.filter(job__posted_by=self.request.user)

class ApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'jobseeker':
            return Application.objects.filter(applicant=self.request.user)
        else:
            return Application.objects.filter(job__posted_by=self.request.user)

class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        job_slug = self.kwargs.get('job_slug')
        job = Job.objects.get(slug=job_slug, status='active')
        
        # Check if already applied
        if Application.objects.filter(job=job, applicant=self.request.user).exists():
            raise serializers.ValidationError("Already applied to this job")
        
        application = serializer.save(
            job=job,
            applicant=self.request.user
        )
        
        # Update job application count
        Job.objects.filter(pk=job.pk).update(applications_count=F('applications_count') + 1)
        
        return application

class ApplicationStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only employers can update status
        return Application.objects.filter(job__posted_by=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def apply_to_job(request, job_slug):
    try:
        job = Job.objects.get(slug=job_slug, status='active')
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.user_type != 'jobseeker':
        return Response({'error': 'Only job seekers can apply'}, status=status.HTTP_403_FORBIDDEN)
    
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return Response({'error': 'Already applied'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ApplicationCreateSerializer(data=request.data)
    if serializer.is_valid():
        application = serializer.save(job=job, applicant=request.user)
        Job.objects.filter(pk=job.pk).update(applications_count=F('applications_count') + 1)
        return Response(ApplicationListSerializer(application).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

urlpatterns = [
    path('', ApplicationListView.as_view(), name='api_application_list'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='api_application_detail'),
    path('<int:pk>/status/', ApplicationStatusUpdateView.as_view(), name='api_application_status'),
    path('apply/<slug:job_slug>/', apply_to_job, name='api_apply_job'),
]
