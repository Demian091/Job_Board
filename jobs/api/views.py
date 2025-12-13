from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from jobs.models import Job, Application, Post, Comment, Like
from company.models import Company
from .serializers import (
    JobSerializer, JobCreateSerializer,
    ApplicationSerializer, ApplicationCreateSerializer,
    PostSerializer, CommentSerializer, LikeSerializer
)


# JOB LIST + CREATE

@api_view(["GET", "POST"])
def jobs_list(request):
    if request.method == "GET":
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    # POST → Only Employers can create jobs
    if request.user.role != "employer":
        return Response({"error": "Only employers can post jobs."}, status=403)

    try:
        company = request.user.company
    except Company.DoesNotExist:
        return Response({"error": "Create your company profile first."}, status=400)

    serializer = JobCreateSerializer(data=request.data)
    if serializer.is_valid():
        job = serializer.save(company=company)
        return Response(JobSerializer(job).data, status=201)

    return Response(serializer.errors, status=400)
# JOB DETAIL

@api_view(["GET"])
def job_detail(request, job_id):
    job = Job.objects.filter(id=job_id).first()
    if not job:
        return Response({"error": "Job not found"}, status=404)

    return Response(JobSerializer(job).data)

# APPLY TO JOB

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_job(request, job_id):
    job = Job.objects.filter(id=job_id).first()
    if not job:
        return Response({"error": "Job not found"}, status=404)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        return Response({"error": "Already applied to this job"}, status=400)

    serializer = ApplicationCreateSerializer(data=request.data)
    if serializer.is_valid():
        app = serializer.save(job=job, applicant=request.user)
        return Response(ApplicationSerializer(app).data, status=201)

    return Response(serializer.errors, status=400)

# GET APPLICANT'S APPLICATIONS

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_applications(request):
    apps = Application.objects.filter(applicant=request.user)
    return Response(ApplicationSerializer(apps, many=True).data)

# EMPLOYER APPLICATIONS

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def employer_applications(request):
    apps = Application.objects.filter(job__company__owner=request.user)
    return Response(ApplicationSerializer(apps, many=True).data)

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employer'

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
