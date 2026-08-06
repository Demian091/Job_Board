from rest_framework import serializers
from apps.applications.models import Application
from apps.api.serializers.jobs import JobListSerializer
from apps.api.serializers.accounts import UserSerializer

class ApplicationListSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant_name', 'status', 'created_at']

class ApplicationDetailSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    applicant = UserSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume', 'portfolio_url', 'linkedin_url',
                  'expected_salary', 'notice_period']

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']
        